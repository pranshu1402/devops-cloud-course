"""
Assignment 2: Automated S3 Bucket Cleanup Using AWS Lambda and Boto3

Objective: To gain experience with AWS Lambda and Boto3 by creating a Lambda function that will automatically clean up old files in an S3 bucket.

Task: Automate the deletion of files older than 30 days in a specific S3 bucket.

Instructions:

1. S3 Setup:
   - Navigate to the S3 dashboard and create a new bucket.
   - Upload multiple files to this bucket, ensuring that some files are older than 30 days (you may need to adjust your system's date temporarily for this or use old files).
2. Lambda IAM Role:
   - In the IAM dashboard, create a new role for Lambda.
   - Attach the `AmazonS3FullAccess` policy to this role. (Note: For enhanced security in real-world scenarios, use more restrictive permissions.)

3. Lambda Function:
   - Navigate to the Lambda dashboard and create a new function.
   - Choose Python 3.x as the runtime.
   - Assign the IAM role created in the previous step.
   - Write the Boto3 Python script to:
     1. Initialize a boto3 S3 client.
     2. List objects in the specified bucket.
     3. Delete objects older than 30 days.
     4. Print the names of deleted objects for logging purposes.

4. Manual Invocation:
   - After saving your function, manually trigger it.
   - Go to the S3 dashboard and confirm that only files newer than 30 days remain.
"""

# Lambda Function Py Script

import boto3
from datetime import datetime

def lambda_handler(event, context):
    try:
        s3_client = boto3.client('s3')
        s3_bucket_name = 'pg_recent_30_bucket'

        bucket_objects = s3_client.list_objects_v2(Bucket=s3_bucket_name)

        for obj in bucket_objects['Contents']:
            obj_key = obj['Key']
            obj_last_modified = obj['LastModified']
            obj_age = (datetime.now() - obj_last_modified).days

            if obj_age > 30:
                s3_client.delete_object(Bucket=s3_bucket_name, Key=obj_key)
                print(f"Deleted object: {obj_key}")
    except Exception as e:
        print(f"Error: {e}")
        raise e