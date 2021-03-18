import boto3, botocore
import os

s3 = boto3.client(
   "s3",
   aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
   aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
)

def upload_pic(files):
    file = files['item_picture']
    output = upload_file_to_s3(file, os.environ.get('S3_BUCKET_NAME'))
    print(str(output))
    return str(output)

def upload_file_to_s3(file, bucket_name, acl='public-read'):
    try:
        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                'ACL': acl,
                'ContentType':file.content_type
            }
        )

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e

    return 'https://' + os.environ.get('S3_BUCKET_NAME') + '.s3.us-east-2.amazonaws.com/' + file.filename 
