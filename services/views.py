from rest_framework.views import APIView
from .serializers import DocumentSerializer
from documents.models import Document
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from documents.views import get_doc_tags
from documents.models import thumbs
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from accounts.models import DumboUser


# Create your views here.
class DocumentAPIUpload(APIView):
    parser_classes = (MultiPartParser, FormParser)

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        docs = Document.objects.filter(owner=request.user)
        serializer = DocumentSerializer(docs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = DocumentSerializer(data=request.data)
        print(request.user)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            doc_object = Document.objects.get(name=serializer.data['name'], owner_id=serializer.data['owner'])
            tags = get_doc_tags(doc_object.path.name)
            if tags is not None:
                doc_object.tags.add(*tags)
                doc_object.save()
            thumb = thumbs(id=doc_object)
            if doc_object.path.name.split('.')[-1] != 'pdf':
                thumb.image = doc_object.path.file
            thumb.save()
            return Response(serializer.data)


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format_=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class PublicDocumentAPI(APIView):
    def get(self, request, *args, **kwargs):
        queried_username = kwargs.get('username', None)
        user = DumboUser.objects.filter(username=queried_username)
        if user:
            docs = Document.objects.filter(is_public=True, owner__username=queried_username)
            serializer = DocumentSerializer(docs, many=True)
            return Response(serializer.data)
        else:
            return Response(data={'Sorry, the requested user does not exist!'})
