from myapp import settings
import boto3
from boto3.session import Session
from botocore.config import Config


class S3:
    def __init__(self):
        self.client: Session = boto3.client('s3',
                                   settings.AWS_REGION,
                                   endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                   aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                   aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                   config=Config(signature_version='s3v4')
                                   )

    def get_presigned_url(self, key: str, time=3600):
        try:
            print('Inside presigned url method=====================================')
            print('s3 object', type(self))
            print('s3 client', type(self.client))
            print('self.client.region_name', self.client)
            print('aws_access_key_id', settings.AWS_ACCESS_KEY_ID, type(settings.AWS_ACCESS_KEY_ID))
            print('aws_secret_access_key', settings.AWS_SECRET_ACCESS_KEY, type(settings.AWS_SECRET_ACCESS_KEY))
            print('object key:', key, type(key))
            print('expire:', time, type(time))
            params = {
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 
                'Key': key
            }
            print('params', params, type(params))
            url =  self.client.generate_presigned_url(ClientMethod='put_object', ExpiresIn=time,
                                                  Params=params)
        except Exception as e:
            e.with_traceback(e.__traceback__)
            print(str(e.__traceback__))
            raise e
        
        return url
        

    def get_file(self, key: str, time=3600):
        return self.client.generate_presigned_url(ClientMethod='get_object', ExpiresIn=time,
                                                  Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': key})

    def delete_file(self, key: str):
        return self.client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=key)