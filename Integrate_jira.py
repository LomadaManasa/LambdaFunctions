import boto3
import requests
import json

def lambda_handler(event, context):
    
    sns_message = json.loads(event['Records'][0]['Sns']['Message'])
    print(sns_message)
    # Extract information from the CloudWatch alarm event
    alarm_name = sns_message['AlarmName']
    alarm_description = sns_message['AlarmDescription']
    
    # Create Jira issue payload
    jira_issue_data = {
        "fields": {
            "project": {
                "key": "TEST"
            },
            "summary": f"{alarm_name}",
            "description": {
                "content": [
                    {
                        "content": [
                            {
                                "text": f"{alarm_description}.",
                                "type": "text"
                                }
                            ],
                            "type": "paragraph"
                        }
                    ],
                    "type": "doc",
                    "version": 1
                
            },
            "issuetype": {
                "name": "Incident"
            }
            # Add other fields as needed
        }
    }
    
    # Make a POST request to the Jira API
    jira_url = "https://mypersonnel.atlassian.net/rest/api/3/issue/"
    jira_auth = ("manasa.lomada1712@gmail.com", "ATATT3xFfGF0dltksXlM2alr2eh1BgFF2FtrLf_cM7CY6PBnKJHR3HIV_yzm_LWEcUJbOWQw9rTlHpT0nemlnROKEDYJm9wXX2s8S9gpq5X2Ew6GgsD8RDaxY7RrL4Stvlu67SszkchtYrpNa7iQnsNqJTMgbbOiaFr4OLdp60UWHmZHE5K4Sxk=3F98EF1A")
    response = requests.post(jira_url, json=jira_issue_data, auth=jira_auth)
    
    if response.status_code == 201:
        print("Jira issue created successfully")
    else:
        print("Failed to create Jira issue:", response.text)
