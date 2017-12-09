import os
import boto3
import json
import urllib.parse
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

SENDER = "Your Name <YOUR.EMAIL>"
RECIPIENT = "YOUR.EMAIL"
SUBJECT = "Turvakamera"
BODY_TEXT = "Turvakameran kuva"
BODY_HTML = """\
<html>
<head></head>
<body>
<p>Turvakameran kuva.</p>
</body>
</html>
"""
CHARSET = "utf-8"

AWS_REGION = "eu-west-1"
client = boto3.client('ses',region_name=AWS_REGION)
s3 = boto3.client('s3')

def handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    print('Checking if both pics are in place ' + key)

    if key.find('_2.jpg') < 0 : return

    print('Both pics found')

    msg = MIMEMultipart('mixed')
    msg['Subject'] = SUBJECT + ' ' + key
    msg['From'] = SENDER
    msg['To'] = RECIPIENT
    msg_body = MIMEMultipart('alternative')

    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)

    msg_body.attach(textpart)
    msg_body.attach(htmlpart)

    msg.attach(msg_body)

    try:
        print('Fetchin pic ' + key)
        s3Response1 = s3.get_object(Bucket=bucket, Key=key)
        att1 = MIMEApplication(s3Response1['Body'].read())
        att1.add_header('Content-Disposition','attachment',filename=key)
        msg.attach(att1)

        key2 = key.replace('_2', '')
        print('Fetching pic ' + key2)
        s3Response2 = s3.get_object(Bucket=bucket, Key=key2)
        att2 = MIMEApplication(s3Response2['Body'].read())
        att2.add_header('Content-Disposition','attachment',filename=key2)
        msg.attach(att2)

        sesResponse = client.send_raw_email(
            Source=SENDER,
            Destinations=[
                RECIPIENT
            ],
            RawMessage={
                'Data':msg.as_string(),
            }
        )
        print(s3Response1)
        print(s3Response2)
        print(sesResponse)
        return 'EmailHandler executed!'
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
    except ClientError as e:
        print(e.response['Error']['Message'])
