pipeline {
    agent {
        docker {
            image 'eddiepease/alpine-python3-pytest'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        CONTAINER_NAME = 'company2vec'
        CONTAINER_TAG = 'latest'
        AWS_ACCOUNT_ID = '341879875473'
        AWS_REGION = 'us-west-2'
        //AWS_ACCESS_KEY_ID     = credentials('jenkins-aws-secret-key-id')
        //AWS_SECRET_ACCESS_KEY = credentials('jenkins-aws-secret-access-key')
    }

    stages {
        stage('Pre-Build Checks') {
            steps {
                // running tests
                sh 'make lint'
                echo "All checks passed"
            }
        }
        stage('Build docker image') {
            steps {
                sh "docker build -t ${CONTAINER_NAME}:${CONTAINER_TAG} --pull --no-cache ."
                echo "Image build complete"
            }
        }
//         stage('Test docker image') {
//             steps {
//                 sh "docker run -d --rm -p $httpPort:$httpPort $containerName:$tag"
//                 echo "Application started on port: ${httpPort} (http)"
//                 echo('NEED TO ADD TEST IN HERE')
//                 sh "docker stop $containerName"
//             }
//         }
        stage('Deploy to AWS ECR') {
            steps {
                script {
                    docker.withRegistry("${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com", "ecr:${AWS_REGION}:${AWS_ACCESS_KEY_ID}") {
                      docker.image("${CONTAINER_NAME}:${CONTAINER_TAG}").push()
                    }
                }
//                 sh "docker tag ${CONTAINER_NAME}:${CONTAINER_TAG} ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${CONTAINER_NAME}:${CONTAINER_TAG}"
//                 sh "docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${CONTAINER_NAME}:${CONTAINER_TAG}"
                echo "Image push complete"
            }
        }
    }
}