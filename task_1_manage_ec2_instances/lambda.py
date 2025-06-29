"""
Assignment 1: Automated Instance Management Using AWS Lambda and Boto3

Objective: In this assignment, you will gain hands-on experience with AWS Lambda and Boto3, Amazon's SDK for Python. You will create a Lambda function that will automatically manage EC2 instances based on their tags.

Task: You're tasked to automate the stopping and starting of EC2 instances based on tags.
Instructions:
1. EC2 Setup:
   - Navigate to the EC2 dashboard and create two new t2.micro instances (or any other available free-tier type).
   - Tag the first instance with a key `Action` and value `Auto-Stop`.
   - Tag the second instance with a key `Action` and value `Auto-Start`.

2. Lambda IAM Role:
   - In the IAM dashboard, create a new role for Lambda.
   - Attach the `AmazonEC2FullAccess` policy to this role. (Note: In a real-world scenario, you would want to limit permissions for better security.)

3. Lambda Function:
   - Navigate to the Lambda dashboard and create a new function.
   - Choose Python 3.x as the runtime.
   - Assign the IAM role created in the previous step.
   - Write the Boto3 Python script to:
     1. Initialize a boto3 EC2 client.
     2. Describe instances with `Auto-Stop` and `Auto-Start` tags.
     3. Stop the `Auto-Stop` instances and start the `Auto-Start` instances.
     4. Print instance IDs that were affected for logging purposes.

4. Manual Invocation:
   - After saving your function, manually trigger it.
   - Go to the EC2 dashboard and confirm that the instances' states have changed according to their tags.
"""

# Lambda Function Py Script

import boto3

def lambda_handler(event, context):
    try:
        ec2_client = boto3.client('ec2')
        ec2_instances = ec2_client.describe_instances()

        for reservation in ec2_instances['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']
                tags = instance['Tags']
                
                action_tag = next((tag['Value'] for tag in tags if tag['Key'] == 'Action'), None)

                if action_tag == 'Auto-Stop':
                    ec2_client.stop_instances(InstanceIds=[instance_id])
                    print(f"Stopped instance: {instance_id}")
                elif action_tag == 'Auto-Start':
                    ec2_client.start_instances(InstanceIds=[instance_id])
                    print(f"Started instance: {instance_id}")
    except Exception as e:
        print(f"Error: {e}")
        raise e