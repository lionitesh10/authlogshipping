import boto3
import datetime

currentDate=str(datetime.datetime.now())[0:10]

s3=boto3.client('s3')
bucket_name='niteshserver-authlogs'
logfile=f'{currentDate}.txt'
s3_key=logfile

s3.upload_file(logfile,bucket_name,s3_key)
