from django.contrib import admin
from django.urls import path, include
from .views import landing_page
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landingpage'),
    path('user/', include('accounts.urls')),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('api/', include('services.urls')),
    path('about', views.about, name='about_page'),
    path('contact', views.contact, name='contact_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
