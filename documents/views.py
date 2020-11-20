from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadDocumentForm, DocumentUpdateForm, DownloadDocumentForm
import requests
from requests.auth import HTTPBasicAuth
from .models import Document, thumbs
from . import utils
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.db.models import Q
from accounts.models import Profile
from django.contrib import messages


# Create your views here.
def get_doc_tags(doc_name: str):
    # doc_name := documents/{name}.ext
    dtype = doc_name.split('.')[-1]
    # gs://dumbo-document-storage/documents/Dark.png
    bucket_name = 'dumbo-document-storage'
    uri = f'gs://{bucket_name}/{doc_name}'
    dest_uri = f'gs://{bucket_name}/tags/ReturnedTags'
    if dtype in ['jpg', 'jpeg', 'png']:
        tags = utils.get_tags(uri, dest_uri, 'image')
    else:
        tags = utils.get_tags(uri, dest_uri, 'document')
    return tags


@login_required(login_url='/user/login')
def my_documents(request):
    form = UploadDocumentForm()
    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc_object = form.save(commit=False)
            doc_object.owner = request.user
            doc_object.save()
            tags = get_doc_tags(doc_object.path.name)
            if tags is not None:
                doc_object.tags.add(*tags)
                doc_object.save()
            thumb = thumbs(id=doc_object)
            print(doc_object.path.name.split('.')[-1])
            if doc_object.path.name.split('.')[-1] != 'pdf':
                thumb.image = doc_object.path.file
            thumb.save()
            return redirect('my_documents')
    context = {'uploadform': form,
               'recent_documents': Document.objects.filter(owner=request.user, in_trash=False).order_by('date_added')[:4],
               'public_documents': Document.objects.filter(is_public=True, owner=request.user, in_trash=False)[:4],
               'most_viewed_documents' : Document.objects.filter(owner=request.user, in_trash=False).order_by('-view_count')[:4],
               'important_documents': Document.objects.filter(is_important=True, owner=request.user, in_trash=False)[:4],
               'common_tags': Document.tags.most_common()[:10],
               'profile': Profile.objects.get(user=request.user),
               'downloadform':DownloadDocumentForm(),
               'thumbs': thumbs.objects.filter(id__owner=request.user, id__in_trash=False)[:4],
               }
    return render(request, 'documents/my_documents.html', context)


class DocumentDetailView(DetailView, UpdateView):
    model = Document
    template_name = 'documents/detail.html'
    fields = ['is_public', 'is_important', 'expiry_date', 'tags']
    success_url = '/user/documents'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        required = Document.objects.get(pk=kwargs['object'].pk)
        required.view_count += 1
        required.save()

        context['uploadform'] = UploadDocumentForm()
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['title'] = 'search'
        context['downloadform'] = DownloadDocumentForm()

        return context

    def form_valid(self, form):
        return super().form_valid(form)


def DownloadFile(request):
    if request.method == 'POST':
        form = DownloadDocumentForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['document_id']
            format = form.cleaned_data['format']
            document = Document.objects.get(owner=request.user, id=id)
            print(document.path.url)
            to_format(document.path.url, document.name, format)
        return redirect('my_documents')
    return redirect('my_documents')


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


class SearchResultsView(ListView):
    model = Document
    template_name = 'documents/search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["uploadform"] = UploadDocumentForm()
        context['common_tags'] = Document.tags.most_common()[:10],
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['title'] = 'search'
        context['downloadfomr'] = DownloadDocumentForm()
        context['thumbs'] = thumbs.objects.filter(id__owner=self.request.user, id__in_trash=False)

        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        print(query)
        query = query.split(" ")  # making a list of all the tags

        condition = Q(tags__name__icontains=query[0])

        for string in query[1:]:
            condition |= Q(tags__name__icontains=string)  # the or condition for all the queried tags

        condition &= Q(owner=self.request.user)  # the and condition for the username

        object_list = Document.objects.filter(condition).distinct()

        return object_list


class FilterResultsView(ListView):
    model = Document
    template_name = 'documents/search_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["uploadform"] = UploadDocumentForm()
        context['common_tags'] = Document.tags.most_common()[:10],
        context['profile'] = Profile.objects.get(user=self.request.user)
        context['title'] = 'search'
        context['downloadfomr'] = DownloadDocumentForm()
        context['thumbs'] = thumbs.objects.filter(id__owner=self.request.user, id__in_trash=False)

        return context

    def get_queryset(self):
        query = self.request.GET.get('q')

        query = query.split("+")  # making a list of all the tags

        condition = Q(tags__name__icontains=query[0])

        for string in query[1:]:
            condition |= Q(tags__name__icontains=string)  # the or condition for all the queried tags

        condition &= Q(owner=self.request.user)  # the and condition for the username

        object_list = Document.objects.filter(condition).distinct()

        return object_list


def toggle_trash(request, pk):
    document = Document.objects.get(pk=pk)
    document.in_trash = not document.in_trash
    document.save()
    if document.in_trash:
        messages.success(request, f'{document.name} is moved to trash')
    else:
        messages.success(request, f'{document.name} is restored')
    return redirect('my_documents')


def delete_document(request, pk):
    document = Document.objects.get(pk=pk)
    if document.in_trash:
        document.delete()
        messages.success(request, f'{document.name} is deleted permanently')
    return redirect('my_documents')


def trashed_documents(request):
    context = {'documents': Document.objects.filter(owner=request.user, in_trash=True),
               'uploadform': UploadDocumentForm(),
               'profile': Profile.objects.get(user=request.user),
               'title': 'trash',
               'thumbs': thumbs.objects.filter(id__owner=request.user,id__in_trash=True),
               }

    return render(request, 'documents/trashed_docs.html', context)
