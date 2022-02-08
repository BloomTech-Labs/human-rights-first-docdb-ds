import os

from botocore.exceptions import ClientError
from dotenv import load_dotenv
from boto3.session import Session


class S3:
    load_dotenv()

    def session(self):
        return Session(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
            aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
        ).client('s3')

    def download(self, bucket_name: str, file_name: str, file_path: str):
        try:
            self.session().download_file(
                Bucket=bucket_name,
                Key=file_name,
                Filename=file_path,
            )
        except ClientError:
            pass
