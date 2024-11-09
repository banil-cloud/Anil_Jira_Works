import os
import requests
import csv
import pandas as pd
import json

JIRA_URL = 'https://jira.com'
JIRA_USER = 'xxxx'
JIRA_PASS = 'XXXXX'

data = pd.read_excel('firstfive.xlsx', engine='openpyxl')

ticket_keys = []
errors = []

with open('mytest.csv', 'a+', newline='') as csvfile:
     # Create a CSV writer object
    writer = csv.writer(csvfile)
    writer.writerow(['Field', 'project_id', 'Assignee', 'Status', 'watcherstatus'])

def write_output(field, project_id,assignee, status, watcherstatus, header):
    with open('mytest.csv', 'a+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([field, project_id, assignee, status, watcherstatus])
    pass

header = True
for index, row in data.iterrows():
    project_id = row['projectid']
    issue_type = row['issuetype']
    summary = row['Summary']
    description = row['Description']
    reporter = row['Reporter']
    assignee = row['Assignee']
    priority = row['Priority']
    components = row['Components']
    scrum_team = row['ScrumTeam']
    due_date = row['DueDate']
    labels = row['Labels']


    print(f"project_id: {project_id}")
    print(f"issue_type: {issue_type}")
    print(f"summary: {summary}")
    print(f"priority: {priority}")



    url = f"{JIRA_URL}/rest/api/2/issue/"
    headers = {'Content-Type': 'application/json'}

    payload = {
        "fields": {
            "project": {
                "key": project_id
            },
            "summary": summary,
            "description": description,
            "issuetype": {
                "name": issue_type
            },
            "assignee": {
                "name": assignee
            },
            "labels": [
                labels
            ],
        }
    }

    # Add 'priority' to payload if it exists
    if priority and not pd.isna(priority):
        payload["fields"]["priority"] = {
            "name": priority
        }
    try: 
        response = requests.post(url, headers=headers, json=payload, auth=(JIRA_USER, JIRA_PASS))
        if response.status_code == 201:
            ticket_creation = response.json()

            url = f"{JIRA_URL}/rest/api/2/issue/{ticket_creation['key']}"
            headers = {'Content-Type': 'application/json'}
            payload =  {
                "fields": {
                    "watcherfield/fieldid": [
                        {
                            "name": "user1"
                        },
                        {
                            "name": "user2"
                        },
                        {
                            "name": "user3"
                        }
                    ]
            }
            }
            
            response = requests.put(url, headers=headers, json=payload, auth=(JIRA_USER, JIRA_PASS))
            if response.status_code == 204:
                write_output(ticket_creation['key'], project_id, assignee, response.status_code, header)
                print(f"Jira ticket created with key: {ticket_creation}")
            else:
                error_response = response.json()
                write_output(ticket_creation['key'], project_id, assignee, response.status_code, header)
                print(f"Error creating Jira ticket: {error_response}")
        else:

            error_response = response.json()
            if 'assignee' in error_response['errors']:
                    payload = {
                        "fields": {
                            "project": {
                                "key": project_id
                            },
                            "summary": summary,
                            "description": description,
                            "issuetype": {
                                "name": issue_type
                            },
                            "labels": [
                                labels
                            ]
                        }
                    }

                    if priority and not pd.isna(priority):
                        payload["fields"]["priority"] = {
                                "name": priority
                            }
                    response = requests.post(url, headers=headers, json=payload, auth=(JIRA_USER, JIRA_PASS))
                    if response.status_code == 201:
                        ticket_creation = response.json()

                        url = f"{JIRA_URL}/rest/api/2/issue/{ticket_creation['key']}"
                        headers = {'Content-Type': 'application/json'}
                        payload =  {
                            "fields": {
                                "watcherfield/fieldid": [
                                    {
                                        "name": "user1"
                                    },
                                    {
                                        "name": "user2"
                                    },
                                    {
                                        "name": "user3"
                                    }
                                ]
                            }
                        }

                        response = requests.put(url, headers=headers, json=payload, auth=(JIRA_USER, JIRA_PASS))
                        if response.status_code == 204:
                            write_output(ticket_creation['key'], project_id, assignee, response.status_code, header)
                            print(f"Jira ticket created with key: {ticket_creation}")
                        else:
                            error_response = response.json()
                            write_output("assignee error", project_id, "project_lead", response.status_code, header)
                            print(f"Error creating Jira ticket: {error_response}")


            if 'components' in error_response['errors']:
                write_output("components error", project_id, assignee, response.status_code, header)
                print(f"Error creating Jira ticket: {error_response}")
            else:
                write_output("assignee error", project_id, "project_lead", response.status_code, header)
                print(f"Error creating Jira ticket: {error_response}")

   
        header = False
    except Exception as e:
        write_output('exception', project_id, assignee, response.status_code, header)
        header = False
        print(f"Error creating Jira ticket: {e}")
