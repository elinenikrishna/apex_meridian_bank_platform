pipeline {
  agent any

  environment {
    PYTHONPATH = "src:."
  }

  stages {
    stage('Install Python Dependencies') {
      steps {
        sh 'python -m pip install --upgrade pip'
        sh 'python -m pip install -r requirements.txt'
      }
    }

    stage('Unit Tests') {
      steps {
        sh 'python -m pytest -q'
      }
    }

    stage('Generate Demo Data') {
      steps {
        sh 'python -m apex_meridian.data_generation.generator --records 1000 --batch-size 500 --domains transactions,customers,merchants --output data/generated/jenkins_smoke'
      }
    }

    stage('Build Images') {
      steps {
        sh 'docker build -f apps/backend/Dockerfile -t apex-meridian-api:${BUILD_NUMBER} .'
        sh 'docker build -f frontend/Dockerfile -t apex-meridian-frontend:${BUILD_NUMBER} .'
      }
    }
  }
}

