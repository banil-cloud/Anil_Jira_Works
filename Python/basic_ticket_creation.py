import requests
from requests.auth import HTTPBasicAuth

# Jira server information
jira_url = 'http://localhost:8080'
username = 'serviceaccount'
password = 'XXXXX'

# Jira issue information
project_key = 'DEV'
summary = 'Issue Summary'
description = 'Issue Description'
issue_type = 'Task'  # You can set the desired issue type (e.g., Bug, Task, Story)

# Create a Jira issue payload
payload = {
    'fields': {
        'project': {
            'key': project_key
        },
        'summary': summary,
        'description': description,
        'issuetype': {
            'name': issue_type
        }
    }
}

# Jira REST API endpoint for creating an issue
create_issue_url = f'{jira_url}/rest/api/2/issue/'

# Make the request to create the issue
response = requests.post(
    create_issue_url,
    json=payload,
    auth=HTTPBasicAuth(username, password),
    headers={'Content-Type': 'application/json'}
)

# Check the response
if response.status_code == 201:
    print(f"Jira issue created successfully! Issue key: {response.json()['key']}")
else:
    print(f"Failed to create Jira issue. Status code: {response.status_code}, Response: {response.text}")
