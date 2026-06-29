pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps { checkout scm }
    }
    stage('Install Dependencies') {
      steps {
        sh '''
          apt-get update -y
          apt-get install -y python3 python3-pip
          pip3 install -r requirements.txt
        '''
      }
    }
    stage('Run Tests') {
      steps {
        sh 'python3 manage.py test calculator'
      }
    }
    stage('Build Docker Image') {
      steps {
        sh 'docker build -t cgpa-calculator:${BUILD_NUMBER} .'
      }
    }
    stage('Deploy') {
      steps {
        sh '''
          docker stop cgpa-api || true
          docker rm cgpa-api || true
          docker run -d -p 8000:8000 \
            --name cgpa-api \
            cgpa-calculator:${BUILD_NUMBER}
        '''
      }
    }
  }
  post {
    success { echo 'Build and deploy succeeded!' }
    failure { echo 'Build failed — check console output.' }
  }
}
