from app.initializers.settings import *
import boto3
from boto3.s3.transfer import S3Transfer

s3_client = boto3.client('s3', 'eu-central-1')
transfer = S3Transfer(s3_client)

def upload_to_s3(local_origin, s3_destination):
	transfer.upload_file(local_origin,S3_BUCKET,s3_destination)	

def download_from_s3(s3_origin, local_destination):
	transfer.download_file(S3_BUCKET, s3_origin, local_destination)