import boto3
import os

# Let's use Amazon S3
s3 = boto3.resource('s3')

def uploadFile(file):
        bucket = 'your-bucket-name'

        data = open(file, 'rb')
        response = s3.Bucket(bucket).put_object(Key=file, Body=data, StorageClass='STANDARD_IA')
        return response;
