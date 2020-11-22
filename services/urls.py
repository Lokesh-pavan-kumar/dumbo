from django.urls import path
from .views import DocumentRestUpload, LoginAPI

urlpatterns = [
    path('', DocumentRestUpload.as_view(), name='document-api-upload'),
    path('login', LoginAPI.as_view(), name='api-login')
]