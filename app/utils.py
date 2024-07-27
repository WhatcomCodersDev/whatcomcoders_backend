import requests
import os

import collections

collections.Iterable = collections.abc.Iterable

from google.cloud import storage


def get_bucket_from_client(
        client: storage.Client, 
        bucket_name: str
        ) -> storage.Bucket:
    photo_bucket = client.bucket(bucket_name)
    return photo_bucket

def setup_gcs_client():
    client = storage.Client()
    return client

def upload_photo_to_bucket(url: str, user_id: str) -> None:
    """Fetches the photo from the given URL and stores it in GCS"""
    client = setup_gcs_client()
    photo_bucket = get_bucket_from_client(client, os.getenv('BUCKET_NAME'))
    print(f"Uploading photo to bucket: {photo_bucket.name}")
    image_response = requests.get(url)
    if image_response.status_code == 200:
        blob = photo_bucket.blob(f'photos/{user_id}.jpg')
        blob.upload_from_string(image_response.content, content_type='image/jpeg')
    else:
        raise Exception(f"Failed to fetch image from {url}")
