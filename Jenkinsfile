pipeline {
  agent any
  options {
    disableResume()
    newContainerPerStage()
    buildDiscarder(logRotator(numToKeepStr: "5"))
  }
  stages {
    stage("Load Conf"){
      steps{
        load "jenkins/${JOB_NAME}-config.groovy"
        dir("jenkins/config"){
          git (
            url: "$CONFIG_GIT_URL",
            branch: "main",
            credentialsId: "$CONFIG_GIT_CREDENTIAL"
          )
          load "config.groovy"
        }
      }
    }
    stage("Build Image") {
      steps {
        script {
          gitCommit = sh(script: "git rev-parse HEAD | cut -c1-8", returnStdout: true).trim()
          authmanAppImage = docker.build("$DOCKER_REGISTRY_URL/authman:${gitCommit}")
        }
      }
    }
    stage("Test") {
      environment {
        MYSQL_DB_CONTAINER_NAME = "mysql_${JOB_NAME}_${BUILD_ID}"
        APP_CONTAINER_NAME = "authman_${JOB_NAME}_${BUILD_ID}"
      }
      steps {
        script {
          docker.image("mysql:${MYSQL_VERSION}").withRun("--name $MYSQL_DB_CONTAINER_NAME -e MYSQL_ROOT_PASSWORD=test -e MYSQL_DATABASE=testing") {
            mysqlContainer -> 
              authmanAppImage.inside("--name $APP_CONTAINER_NAME -e FLASK_APP=authman -e FLASK_ENV=testing -e FLASK_DEBUG=1 -e AUTHMAN_DATABASE_URI=mysql+pymysql://root:test@$MYSQL_DB_CONTAINER_NAME:3306/testing --link ${mysqlContainer.id}"){
                retry(100){
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
            authmanAppImage.push()
          }
        }
      }
    }
    stage("First time Deployment") {
      when {
        equals expected: 1, actual: currentBuild.number
      }
      steps {
        echo 'Deploy'
        // ansiblePlaybook(inventory: 'scripts/deployment/inventory.ini', playbook: 'scripts/deployment/playbook.yaml')
      }
    }
  }
}
