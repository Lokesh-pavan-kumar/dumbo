from django.urls import path
from .views import DocumentAPIUpload, LoginAPI, PublicDocumentAPI

urlpatterns = [
    path('login', LoginAPI.as_view(), name='api-login'),
    path('search/<str:username>/', PublicDocumentAPI.as_view(), name='user-public-docs'),
    path('upload', DocumentAPIUpload.as_view(), name='document-api-upload'),
]