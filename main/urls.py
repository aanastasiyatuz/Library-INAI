from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import index

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('library/', include('library.urls')),
    path('account/', include('account.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# sudo systemctl restart nginx
# sudo systemctl restart gunicorn
# sudo systemctl daemon-reload
# sudo systemctl restart gunicorn
