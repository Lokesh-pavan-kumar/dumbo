from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadDocumentForm, DocumentUpdateForm, DownloadDocumentForm
from .models import Document, thumbs
from . import utils
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.db.models import Q
from accounts.models import Profile
from django.contrib import messages
from .forms import ImportantTagsForm
from .doc_conversion import getConvertedImage


def storage_access(user_profile, doc):
    storage_limit = user_profile.total_space
    used_space = user_profile.used_space
    doc_space = doc.path.size
    if used_space + doc_space < storage_limit:
        user_profile.used_space += doc_space
        user_profile.save()
        return True
    return False


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
    profile = Profile.objects.get(user=request.user)
    storage_exceeded = True if profile.used_space >= profile.total_space else False
    if request.method == 'POST':
        form = UploadDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc_object = form.save(commit=False)
            doc_object.owner = request.user
            doc_object.save()
            has_storage_access = storage_access(profile, doc_object)
            if has_storage_access:
                tags = get_doc_tags(doc_object.path.name)
                if tags is not None:
                    doc_object.tags.add(*tags)
                    doc_object.save()
                thumb = thumbs(id=doc_object)
                print(doc_object.path.name.split('.')[-1])
                if doc_object.path.name.split('.')[-1] != 'pdf':
                    thumb.image = doc_object.path.file
                thumb.save()
            else:
                doc_object.delete()
                print('Storage Exceeded')
                messages.warning(request, f'Sorry! Please upgrade your storage plan to upload more documents!')
            return redirect('my_documents')
    context = {'uploadform': form,
               'recent_documents': Document.objects.filter(owner=request.user, in_trash=False).order_by('date_added')[
                                   :4],
               'public_documents': Document.objects.filter(is_public=True, owner=request.user, in_trash=False)[:4],
               'most_viewed_documents': Document.objects.filter(owner=request.user, in_trash=False).order_by(
                   '-view_count')[:4],
               'important_documents': Document.objects.filter(is_important=True, owner=request.user, in_trash=False)[
                                      :4],
               'common_tags': Document.tags.most_common()[:10],
               'profile': profile,
               'downloadform': DownloadDocumentForm(),
               'thumbs': thumbs.objects.filter(id__owner=request.user, id__in_trash=False),
               'storage_exceeded': storage_exceeded,
               'remaining_space': round((profile.total_space - profile.used_space) * 1e-6, 2),
               'total_space': profile.total_space * 1e-6,
               'data_value': 100 - ((profile.total_space - profile.used_space) / profile.total_space) * 100,
               'add_tag_form': ImportantTagsForm()
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
            format_ = form.cleaned_data['format']
            document = Document.objects.get(owner=request.user, id=id)
            print(document.path.url)
            if format_ != 'pdf':
                url = getConvertedImage(document.path.url, document.name, format_)
            else:
                url = getConvertedImage(document.path.url, document.name)
            messages.success(request, f"Download at <a href='{url}'>link</a>", extra_tags='safe')
        return redirect('my_documents')
    return redirect('my_documents')


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
        context['q'] = query = self.request.GET.get('q')
        context['remaining_space'] = round((Profile.objects.get(user=self.request.user).total_space - Profile.objects.get(user=self.request.user).used_space) * 1e-6, 2),
        context['total_space'] = Profile.objects.get(user=self.request.user).total_space * 1e-6,
        context['data_value'] = 100 - ((Profile.objects.get(user=self.request.user).total_space - Profile.objects.get(user=self.request.user).used_space) / Profile.objects.get(user=self.request.user).total_space) * 100,

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
        context['q'] = self.request.GET.get('q')
        context['remaining_space'] = round((Profile.objects.get(
            user=self.request.user).total_space - Profile.objects.get(user=self.request.user).used_space) * 1e-6, 2),
        context['total_space'] = Profile.objects.get(user=self.request.user).total_space * 1e-6,
        context['data_value'] = 100 - ((Profile.objects.get(user=self.request.user).total_space - Profile.objects.get(
            user=self.request.user).used_space) / Profile.objects.get(user=self.request.user).total_space) * 100,

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
               'thumbs': thumbs.objects.filter(id__owner=request.user, id__in_trash=True),
               }

    return render(request, 'documents/trashed_docs.html', context)


def add_important_tag(request):
    if request.method == 'POST':
        form = ImportantTagsForm(request.POST)
        profile = Profile.objects.get(user=request.user)

        if form.is_valid():
            tag = form.cleaned_data['tag']

            if tag is not None:
                profile.important_tags.add(tag)
                profile.save()

    return redirect('my_documents')
