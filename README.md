# AWS ECS event status change alert for Slack

A simple AWS Lambda function to send Slack notification when ECS service status changes.

## How it works

This function is triggered by CloudWatch Events when ECS service status changes.

It sends a Slack notification to a specified channel with the following information.

- Service name
- Cluster name
- Task definition with revision
- Status
- Event name
- Event message
- Time
- Link to the ECS Task

The pipeline is as follows.

- ECS service status changes
- AWS Event Bridge sends a message to AWS Simple Notification Service (SNS)
- SNS sends a message to AWS Lambda
- Lambda function sends a message via Slack Webhook API

## How to use it

### 1. Create a Slack app and create a webhook

- Create a Slack app and install it to your workspace from [here](https://api.slack.com/apps).
- Create a Slack webhook from [here](https://api.slack.com/messaging/webhooks).

### 2. Before you start with AWS

You need to create all the resources in the same region. If you have multiple regions, where you have ECS services, you need to create AWS Event Bridge where you pipe all the events from all the regions to one region where you have the Lambda function and SNS topic.

### 3. Create a Lambda function

- Author from scratch
- Runtime: Python
- Function code: `lambda_function.py`
- Replace the following variables with your own values
  - `CLUSTERNAME`
  - `SLACK_WEBHOOK_URL`

### 4. Create a SNS topic

- Name: Create topic
- Type: Standard

### 6. Create a subscription for the SNS topic

- Protocol: Lambda
- Copy the ARN of the Lambda function

### 7. Create a AWS Event Bridge rule

- Rule with Event Pattern
- You find the pattern in `eventbridge-pattern.json`
- Target: Select SNS topic and the topic you created in step 4

## Finished

Now you should be able to see the Slack notification when ECS service status changes.

## License

MIT License. See LICENSE file.
