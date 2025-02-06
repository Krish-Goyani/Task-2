import os
from google.cloud import storage
from src.app.config.settings import settings

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = settings.SERVICE_ACCOUNT_JSON


BUCKET_NAME = settings.BUCKET_NAME

class GoogleCloudStorage:
    
    def upload_image(self, file, file_name: str) -> str:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(file_name)
        blob.upload_from_file(file)
        return blob.public_url
