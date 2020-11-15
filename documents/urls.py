from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.my_documents, name='my_documents'),
    path('detail/<pk>/', views.DocumentDetailView.as_view(), name="detail"),
    path('search', views.SearchResultsView.as_view(), name="search_results"),
]
