"""
Assignment 6: Monitor and Alert High AWS Billing Using AWS Lambda, Boto3, and SNS

Objective: Create an automated alerting mechanism for when your AWS billing exceeds a certain threshold.

Task: Set up a Lambda function to check your AWS billing amount daily, and if it exceeds a specified threshold, send an alert via SNS.

Instructions:

1. SNS Setup:
   - Navigate to the SNS dashboard and create a new topic.
   - Subscribe your email to this topic.
   2. Lambda IAM Role:
      - In the IAM dashboard, create a new role for Lambda.
      - Attach policies that allow reading CloudWatch metrics and sending SNS notifications.
   3. Lambda Function:
      - Navigate to the Lambda dashboard and create a new function.
      - Choose Python 3.x as the runtime.
      - Assign the IAM role created in the previous step.
      - Write the Boto3 Python script to:
        1. Initialize boto3 clients for CloudWatch and SNS.
        2. Retrieve the AWS billing metric from CloudWatch.
        3. Compare the billing amount with a threshold (e.g., $50).
        4. If the billing exceeds the threshold, send an SNS notification.
        5. Print messages for logging purposes.
   4. Event Source (Bonus):
      - Attach an event source, like Amazon CloudWatch Events, to trigger the Lambda function daily.
   5. Testing:
      - Manually trigger the Lambda function or wait for the scheduled event.
      - If your billing is over the threshold, you should receive an email alert.
"""

# Lambda Function Py Script
import boto3
import datetime
import os

ONE_DAY_IN_SECONDS = 86400
BILLING_THRESHOLD = 50.0
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

def lambda_handler(event, context):
    cloudwatch_client = boto3.client('cloudwatch')
    sns_client = boto3.client('sns')

    end = datetime.datetime.now()
    start = end - datetime.timedelta(days=1)


    try:
        response = cloudwatch_client.get_metric_statistics(
            Namespace='AWS/Billing',
            MetricName='EstimatedCharges',
            Dimensions=[
                {'Name': 'Currency', 'Value': 'USD'}
            ],
            StartTime=start,
            EndTime=end,
            Period=ONE_DAY_IN_SECONDS,
            Statistics=['Maximum']
        )

        datapoints = response.get('Datapoints', [])
        if not datapoints:
            print("No billing data available yet.")
            return

        latest = max(datapoints, key=lambda x: x['Timestamp'])
        amount = latest['Maximum']
        print(f"Current billing amount: ${amount:.2f}")

        if amount > BILLING_THRESHOLD:
            message = f"ALERT: AWS Billing exceeded threshold! Current charges: ${amount:.2f}"
            print(message)

            sns_client.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="AWS Billing Alert",
                Message=message
            )
        else:
            print("Billing is under control.")

    except Exception as e:
        print(f"Error fetching billing data or sending notification: {e}")
