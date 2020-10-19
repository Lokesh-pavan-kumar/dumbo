from django.urls import path
from .views import register, login_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    # URLs are of the form users/<name>
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
]
