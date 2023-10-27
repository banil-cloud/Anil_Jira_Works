pipeline {
    agent any

    environment {
        // Define the Jira credentials from the stored credentials ID
        JIRA_CREDENTIALS = credentials('anil2')
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Check out your code from the public GitHub repository
                git branch: 'main', url: 'https://github.com/banil-cloud/testing.git'
            }
        }

        stage('Execute Code') {
            steps {
                script {
                    // Make the script executable
                    sh 'chmod +x ticketcreation.sh'
                    
                    // Use 'withCredentials' to securely provide Jira credentials to the script
                    withCredentials([usernamePassword(credentialsId: 'anil123', passwordVariable: 'JIRA_PASSWORD', usernameVariable: 'JIRA_USERNAME')]) {
                        // Execute your script while passing Jira credentials as environment variables
                        sh './ticketcreation.sh'
                    }
                }
            }
        }

        stage('Provide Response') {
            steps {
                // Print a response or capture any output from the code execution
                sh 'echo "Code execution completed."'
            }
        }
    }
}