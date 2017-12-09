# Security Camera

Readme very much in progress. Just like serverless.

## Raspberry Pi

With PIR motion sensor and camera. Python code.

## AWS

### S3

Stores the pics

### lambda

Python code. Executes when new file is uploaded into S3. Forwards the pics to SES.

### SES

Emails me the pics

### CloudWatch

Logs print statements
