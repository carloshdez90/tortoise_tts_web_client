import os
from google.cloud import storage

BUCKET="tortoise-tts"

def get_folder_list(prefix=None):

    client = storage.Client()

    if prefix is not None:
        blobs = client.list_blobs(BUCKET, prefix=prefix)
        folders = sorted(list(set([k.name for k in blobs])))

        #if len(folders) == 1: #has 

    else:
        blobs = client.list_blobs(BUCKET)
        folders = sorted(list(set([k.name.split('/')[0] for k in blobs])))

    return folders
