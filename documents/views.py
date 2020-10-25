from django.shortcuts import render, redirect
from .forms import UploadDocumentForm
from django.core.files.storage import FileSystemStorage
import requests
from requests.auth import HTTPBasicAuth
from .models import Document


# Create your views here.
def my_documents(request):
    form = UploadDocumentForm()
    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc_object = form.save(commit=False)
            doc_object.owner = request.user
            doc_object.save()

            return redirect('landingpage')
    context = {'form': form, 'documents': Document.objects.all()}
    return render(request, 'documents/my_documents.html', context)


def to_format(file_path: str, name: str, format_: str = 'pdf'):
    api_key = '830dd544d855f1bb095949ecbd165a8f54b446b1'
    job_id = start_job(api_key, file_path, format_)
    target_file_id = conversion(api_key, job_id)
    download_file(api_key, target_file_id, name, format_)


def start_job(api_key: str, file_path: str, format_: str = 'pdf'):
    endpoint = "https://sandbox.zamzar.com/v1/jobs"
    target_format = format_

    file_content = {'source_file': open(file_path, 'rb')}
    data_content = {'target_format': target_format}
    r = requests.post(endpoint, data=data_content, files=file_content, auth=HTTPBasicAuth(api_key, ''))
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
    local_filename = f'{name}.{format_}'
    endpoint = f'https://sandbox.zamzar.com/v1/files/{target_file_id}/content'

    response = requests.get(endpoint, stream=True, auth=HTTPBasicAuth(api_key, ''))

    try:
        with open(local_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
            print('File Downloaded and Saved')
    except IOError:
        print('Error')
