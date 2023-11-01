pipeline {
    agent any

    environment {
        // Define the Jira credentials from the stored credentials ID
        JIRA_CREDENTIALS = credentials('XXX')
    }

    stages {
        stage('Prompt for Project Key') {
            steps {
                script {
                    def projectKey
                    // Keep prompting until a non-empty project key is provided
                    while (true) {
                        def userInput = input message: 'Please enter the Jira project key:', parameters: [string(description: 'Jira Project Key', name: 'PROJECT_KEY')]
                        projectKey = userInput
                        if (projectKey && !projectKey.trim().isEmpty()) {
                            break
                        }
                        echo "Invalid input. Project key cannot be empty. Please provide a valid project key."
                    }
                    currentBuild.description = "Jira Project Key: $projectKey"
                    // Set the environment variable with the correct name
                    env.PROJECT_KEY = projectKey
                }
            }
        }

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
                    def projectKey = env.PROJECT_KEY  // Declare the variable inside the script block
                    
                    // Use 'withCredentials' to securely provide Jira credentials to the script
                    withCredentials([usernamePassword(credentialsId: 'XXX', passwordVariable: 'JIRA_PASSWORD', usernameVariable: 'JIRA_USERNAME')]) {
                        // Execute your script while passing Jira credentials and project key as environment variables
                        sh "./ticketcreation.sh $projectKey"
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
