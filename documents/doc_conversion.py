import requests
from requests.auth import HTTPBasicAuth
from google.cloud import storage
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credential.json"


def to_format(file_path: str, name: str, format_: str = 'pdf'):
    api_key = '2c87cd6e261cd7251931427f6695ee53a6c907ea'
    # 830dd544d855f1bb095949ecbd165a8f54b446b1 -- Tarun
    job_id = start_job(api_key, file_path, format_)
    target_file_id = conversion(api_key, job_id)
    return download_file(api_key, target_file_id, name, format_)


def start_job(api_key: str, file_path: str, format_: str = 'pdf'):
    endpoint = "https://sandbox.zamzar.com/v1/jobs"
    target_format = format_
    source_file = file_path

    data_content = {'source_file': source_file, 'target_format': target_format}
    r = requests.post(endpoint, data=data_content, auth=HTTPBasicAuth(api_key, ''))
    json_resp = r.json()
    job_id = json_resp['id']
    # source_file_id = json_resp['source_file']['id']
    return job_id


def conversion(api_key: str, job_id: int):
    endpoint = f'https://sandbox.zamzar.com/v1/jobs/{job_id}'
    while True:
        r = requests.get(endpoint, auth=HTTPBasicAuth(api_key, ''))
        json_resp = r.json()
        status = json_resp['status']
        if status == 'successful':
            target_files = json_resp['target_files']
            target_file_id = target_files[0]['id']
            return target_file_id
        else:
            continue


def download_file(api_key: str, target_file_id: int, name: str, format_: str = 'pdf'):
    local_filename = f'files/{name}.{format_}'
    endpoint = f'https://sandbox.zamzar.com/v1/files/{target_file_id}/content'

    response = requests.get(endpoint, stream=True, auth=HTTPBasicAuth(api_key, ''))
    storage_client = storage.Client()
    bucket = storage_client.bucket('dumbo-document-storage')
    blob = bucket.blob(local_filename)

    try:
        blob.upload_from_string(response.content)
    except IOError:
        print('Error')

    return blob.name


def getConvertedImage(path, name, format_='pdf'):
    uri = 'https://storage.googleapis.com/dumbo-document-storage/'
    return uri + to_format(path, name, format_)



