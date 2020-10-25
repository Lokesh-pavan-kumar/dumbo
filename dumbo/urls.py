from django.contrib import admin
from django.urls import path, include
from .views import landing_page
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landingpage'),
    path('user/', include('accounts.urls')),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('documents/', include('documents.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
