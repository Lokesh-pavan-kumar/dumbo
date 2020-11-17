from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_documents, name='my_documents'),
    path('detail/<int:pk>/', views.DocumentDetailView.as_view(), name="detail"),
    path('search', views.SearchResultsView.as_view(), name="search_results"),
    path('toggle-trash/<int:pk>', views.toggle_trash, name='toggle-trash'),
    path('delete-document/<int:pk>', views.delete_document, name='delete-document'),
    path('trash', views.trashed_documents, name='trash'),
    path('download', views.DownloadFile, name="download_file"),
]
