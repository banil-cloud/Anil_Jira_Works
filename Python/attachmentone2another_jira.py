import requests
from requests.auth import HTTPBasicAuth

# Jira Server A details (source)
jira_a_url = "https://anil.atlassian.net"
jira_a_user = "anil@gmail.com"
jira_a_token = "xxxxxx"
source_issue_key = "LIN-4"

# Jira Server B details (destination)
jira_b_url = "https://m.atlassian.net"
jira_b_user = "m@gmail.com"
jira_b_token = "xxxxx"
target_issue_key = "KBB-2"

# Step 1: Get attachments from Server A
attachments_api_a = f"{jira_a_url}/rest/api/2/issue/{source_issue_key}?fields=attachment"
response_a = requests.get(attachments_api_a, auth=HTTPBasicAuth(jira_a_user, jira_a_token))

try:
    response_a.raise_for_status()
    issue_data = response_a.json()
    attachments = issue_data['fields'].get('attachment', [])
except requests.exceptions.RequestException as e:
    print(f"❌ Failed to get attachments from {source_issue_key} - {e}")
    exit(1)
except ValueError:
    print("❌ Response is not in JSON format. Check if the Jira Server A is running and responding correctly.")
    print("Response content:\n", response_a.text)
    exit(1)

if not attachments:
    print(f"ℹ️ No attachments found in issue {source_issue_key}")
else:
    for attachment in attachments:
        file_url = attachment['content']
        file_name = attachment['filename']

        print(f"⬇️ Downloading: {file_name} from {file_url}")
        file_data = requests.get(file_url, auth=HTTPBasicAuth(jira_a_user, jira_a_token))

        if file_data.status_code != 200:
            print(f"❌ Failed to download '{file_name}' - Status: {file_data.status_code}")
            continue

        # Step 2: Upload to Server B
        upload_url_b = f"{jira_b_url}/rest/api/2/issue/{target_issue_key}/attachments"
        headers_b = {
            "X-Atlassian-Token": "no-check",
            "Accept": "application/json"
        }
        files = {
            'file': (file_name, file_data.content)
        }

        upload_response = requests.post(
            upload_url_b,
            headers=headers_b,
            auth=HTTPBasicAuth(jira_b_user, jira_b_token),
            files=files
        )

        if upload_response.status_code in [200, 201]:
            print(f"✅ Uploaded '{file_name}' to issue {target_issue_key}")
        else:
            print(f"❌ Failed to upload '{file_name}' - Status: {upload_response.status_code}")
            print("Response:", upload_response.text)
