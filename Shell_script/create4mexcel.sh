#!/bin/bash
set -x
user="username"
pass="password"

tail -n +2 input.csv | while IFS="," read -r projectid issuetype Summery Description Reporter Assignee  Priority Components Teams DueDate Labels
do

ticketcreation=$(curl -s -L -X POST -u $user:$pass -H "Content-Type: application/json" "https://jira.com/rest/api/2/issue" -d '{
    "fields": {
        "project":
        {
            "key": "'$projectid'"
        },
        "summery": "'$summery'",
        "description": "'$description'",
        "issuetype": {
            "name": '"$issuetype'"
        },
        "priority": {
            "name": "'$Priority'"
        },
        "labels": [
            "'$Labels'"
            ],
        "assignee": {
            "name": "'$Assignee'"
        }
    }
}' -w '%{http_code}\n' -s)

echo $ticketcreation
done
