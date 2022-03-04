pipeline {
  agent any
  options {
    disableResume()
    newContainerPerStage()
    buildDiscarder(logRotator(numToKeepStr: "5"))
  }
  parameters {
    string(name: "MYSQL_TEST_DATABASE", defaultValue: "authman", description: "Name of mysql test container")
    password(name: "MYSQL_TEST_PASSWORD", defaultValue: "root", description: "MySQL test container root password")
  }
  stages {
    stage("Load Conf"){
      steps{
        load "jenkins/envs/${JOB_NAME}.groovy"
      }
    }
    stage("Build Image") {
      steps {
        script {
          DOCKER_IMAGE = docker.build($IMAGE_NAME)
        }
      }
    }
    stage("Test") {
      environment {
        MYSQL_DB_CONTAINER_NAME = "jenkins_mysql_${JOB_NAME}_${BUILD_ID}"
      }
      steps {
        script {
          docker.image("mysql").withRun("-e MYSQL_ROOT_PASSWORD=$params.MYSQL_TEST_PASSWORD -e MYSQL_DATABASE=$params.MYSQL_TEST_DATABASE --name $MYSQL_DB_CONTAINER_NAME") { c ->
            docker.image(params.IMAGE_NAME).inside("--link ${c.id} -e AUTHMAN_DATABASE_URI=mysql+pymysql://root:$params.MYSQL_TEST_PASSWORD@$MYSQL_DB_CONTAINER_NAME/$params.MYSQL_TEST_DATABASE") {
              retry(100) {
                sh "sleep 3"
                sh "flask app testdb"
              }
              sh "flask db upgrade"
              sh "coverage run -m pytest"
              sh "coverage html"
              archiveArtifacts artifacts: "htmlcov/", fingerprint: true
              publishHTML target: [
                allowMissing: false,
                alwaysLinkToLastBuild: false,
                keepAll: true,
                reportDir: "htmlcov",
                reportFiles: "index.html",
                reportName: "Code Coverage"
                ]
            }
          }
        }
      }
    }
    stage("Push Image") {
      steps {
        script {
          docker.withRegistry("", "dockerhub") {
            DOCKER_IMAGE.push()
          }
        }
      }
    }
    stage("First time Deployment") {
      when {
        equals expected: 1, actual: currentBuild.number
      }
      steps {
        ansiblePlaybook(inventory: 'scripts/deployment/inventory.ini', playbook: 'scripts/deployment/playbook.yaml')
      }
    }
  }
}
