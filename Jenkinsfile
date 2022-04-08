pipeline {
  agent any
  options {
    disableResume() // Do not allow the pipeline to resume if the controller restarts.
    newContainerPerStage()  // Used with docker or dockerfile top-level agent. When specified, each stage will run in a new container instance on the same node, rather than all stages running in the same container instance.
    buildDiscarder(logRotator(numToKeepStr: "5")) // Keep 5 last build
  }
  triggers {
    pollSCM 'H/15 * * * *'  // Check git for last changes every 15 miuntes
  }
  stages {
    stage("Load Conf"){
      steps{
        load "jenkins/${JOB_NAME}-config.groovy" // Load some ENVs such as CONFIG_GIT_URL, CONFIG_GIT_CREDENTIAL and MYSQL_VERSION
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
          gitCommit = sh(script: "git rev-parse HEAD | cut -c1-7", returnStdout: true).trim()
          authmanAppImage = docker.build("${DOCKER_REGISTRY_ADDRESS}/authman:${gitCommit}")
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
            mysqlContainer -> authmanAppImage.inside("--name $APP_CONTAINER_NAME -e FLASK_APP=authman -e FLASK_ENV=testing -e FLASK_DEBUG=1 -e AUTHMAN_DATABASE_URI=mysql+pymysql://root:test@$MYSQL_DB_CONTAINER_NAME:3306/testing --link ${mysqlContainer.id}"){
              retry(100){
                sh "sleep 5"
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
              sh "coverage xml"
              cobertura (
                coberturaReportFile: "coverage.xml"
              )
            }
          }
        }
      }
    }
    stage("Push Image") {
      steps {
        script {
            authmanAppImage.push()
            authmanAppImage.push("latest")
            gitTag = sh(script: "git tag --points-at HEAD", returnStdout: true).trim()
            if (gitTag !="") {
              gitTag = gitTag.minus("v")
              appVersionMajor = gitTag.split("\\.")[0]
              appVersionMinor = gitTag.split("\\.")[0] + "." + gitTag.split("\\.")[1]
              appVersionPatch = gitTag.split("\\.")[0] + "." + gitTag.split("\\.")[1] + "." + gitTag.split("\\.")[2]
              authmanAppImage.push(appVersionMajor)
              authmanAppImage.push(appVersionMinor)
              authmanAppImage.push(appVersionPatch)
            }
        }
      }
    }
  }
}
