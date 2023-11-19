#!/usr/bin/python3.6
import urllib3
import json
import time
http = urllib3.PoolManager()
def lambda_handler(event, context):
    url = "SLACK_WEBHOOK_URL"
    snsMessage = json.loads(event['Records'][0]['Sns']['Message'])

    taskId = snsMessage['detail']['taskArn'].split('/')[-1]
    taskDef = snsMessage['detail']['taskDefinitionArn'].split('/')[-1]

    link = "https://eu-central-1.console.aws.amazon.com/ecs/home?region=eu-central-1#/clusters/CLUSTERNAME/tasks/"+taskId+"/details"
    service = snsMessage['detail']['group'].split(':')[1]
    lastStatus = snsMessage['detail']['lastStatus']
    messageText = ""
    color = ""
    if lastStatus=='STOPPED':
        color = "#F44336"
        stoppedReason = snsMessage['detail']['stoppedReason']
        messageText = lastStatus +" - "+ stoppedReason + " <!channel>"
    elif lastStatus=='PENDING':
        color = "#FF9800"
        messageText = lastStatus
    elif lastStatus=='RUNNING':
        color = "#4CAF50"
        messageText = lastStatus
    else:
        messageText = lastStatus
    
    
    msg = {
        "text":"",
        "channel": "#aws-events",
        "username": "AWS Events",
        "attachments": [
            {
                "author_name":taskDef,
                "color": color,
                "title": service,
                "title_link": link,
                "text":messageText,
                "footer": "AWS Events",
                "ts": round(time.time() * 1000)
            }
        ]
    }


    encoded_msg = json.dumps(msg).encode('utf-8')
    resp = http.request('POST',url, body=encoded_msg)