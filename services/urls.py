from django.urls import path
from .views import DocumentRestUpload, LoginAPI, PublicDocumentAPI

urlpatterns = [
    path('search/<str:username>/', PublicDocumentAPI.as_view(), name='user-public-docs'),
    path('upload', DocumentRestUpload.as_view(), name='document-api-upload'),
    path('login', LoginAPI.as_view(), name='api-login')
]