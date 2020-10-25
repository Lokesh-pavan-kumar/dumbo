from django.shortcuts import render, redirect
from .forms import UploadDocumentForm
from django.core.files.storage import FileSystemStorage
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
