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


# Create your views here.
class DocumentRestUpload(APIView):
    parser_classes = (MultiPartParser, FormParser)

    # permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        docs = Document.objects.filter(is_public=True)
        serializer = DocumentSerializer(docs, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
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

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)
