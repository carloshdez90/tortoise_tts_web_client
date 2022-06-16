import os
import datetime
from google.cloud import storage

BUCKET="tortoise-tts"

def get_folder_list(prefix=None):

    client = storage.Client()

    if prefix is not None:
        blobs = client.list_blobs(BUCKET, prefix=prefix)
        folders = sorted(list(set([k.name for k in blobs])))

    else:
        blobs = client.list_blobs(BUCKET)
        folders = sorted(list(set([k.name.split('/')[0] for k in blobs])))

    return folders

def upload_file(destination, file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET)
    blob = bucket.blob(destination)

    blob.upload_from_filename(file_name)


def generate_download_signed_urls(blob_list):
    """
    Generates a v4 signed URL for downloading a blob.
    """

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET)
    signed_urls = []
    for blob_name in blob_list:
        blob = bucket.blob(blob_name)

        url = blob.generate_signed_url(
            version="v4",
            # This URL is valid for 30 minutes
            expiration=datetime.timedelta(minutes=30),
            # Allow GET requests using this URL.
            method="GET",
        )
        signed_urls.append({
                            'filename': blob_name.split('/')[-1],
                            'signed_url': url
                            })

    return signed_urls