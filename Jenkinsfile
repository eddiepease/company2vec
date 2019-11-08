pipeline {
    agent any

    environment {
        CONTAINER_NAME = 'company2vec'
        CONTAINER_TAG = 'latest'
        AWS_ACCOUNT_ID = '341879875473'
        AWS_REGION = 'us-west-2'
    }

    stages {
        stage('Pre-Build Checks') {
            steps {
                // running tests
                sh 'pylint kleinapp.py --disable=E0401,C0103,W0613'
	            sh 'pylint app --disable=E0401,W0613,W0201,R0903'
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
                withAWS(credentials:'dc7d59a2-89eb-4fbb-9205-116b02d6cc8f') {
                    sh '$(aws ecr get-login --no-include-email --region ${AWS_REGION})'
                    sh "docker tag ${CONTAINER_NAME}:${CONTAINER_TAG} ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${CONTAINER_NAME}:${CONTAINER_TAG}"
                    sh "docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${CONTAINER_NAME}:${CONTAINER_TAG}"
                }
                echo "Image push complete"
            }
        }
    }
}