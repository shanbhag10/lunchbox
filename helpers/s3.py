import boto3, botocore
from datetime import datetime
import os
import random

s3 = boto3.client(
   "s3",
   aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
   aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
)


def upload_pic(file, user_id, name):
    if file == None or file.filename == "":
        return ""

    output = upload_file_to_s3(file, user_id, name, os.environ.get('S3_BUCKET_NAME'))
    return str(output)


def upload_file_to_s3(file, user_id, name, bucket_name, acl='public-read'):
    try:
        filename = str(user_id) + '_' + name + '_' + str(datetime.now())
        s3.upload_fileobj(
            file,
            bucket_name,
            filename,
            ExtraArgs={
                'ACL': acl,
                'ContentType':file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("S3 Error: ", e)
        return e

    return 'https://' + os.environ.get('S3_BUCKET_NAME') + '.s3.us-east-2.amazonaws.com/' + filename
