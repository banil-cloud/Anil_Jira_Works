#!/bin/bash

# Jira server information
JIRA_URL="http://localhost:8080"
USERNAME="serviceaccount"
PASSWORD="XXXX"

# Jira issue information
PROJECT_KEY="DEV"
SUMMARY="Issue Summary"
DESCRIPTION="Issue Description"
ISSUE_TYPE="Task"

# Jira REST API endpoint for creating an issue
CREATE_ISSUE_URL="${JIRA_URL}/rest/api/2/issue/"

# Create a JSON payload for the Jira issue
PAYLOAD='{
  "fields": {
    "project": {
      "key": "'"${PROJECT_KEY}"'"
    },
    "summary": "'"${SUMMARY}"'",
    "description": "'"${DESCRIPTION}"'",
    "issuetype": {
      "name": "'"${ISSUE_TYPE}"'"
    }
  }
}'

# Make the request to create the issue using curl
RESPONSE=$(curl -s -u "${USERNAME}:${PASSWORD}" -H "Content-Type: application/json" -X POST --data "${PAYLOAD}" "${CREATE_ISSUE_URL}")

# Check the response
if [[ "${RESPONSE}" == *"key"* ]]; then
  ISSUE_KEY=$(echo "${RESPONSE}" | awk -F'"' '/key/{print $4}')
  echo "Jira issue created successfully! Issue key: ${ISSUE_KEY}"
else
  ERROR_MESSAGE=$(echo "${RESPONSE}" | awk -F'"' '/errorMessages/{print $4}' 2>/dev/null || echo "${RESPONSE}")
  echo "Failed to create Jira issue. Error message: ${ERROR_MESSAGE}"
fi
