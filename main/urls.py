from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import index, qr

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('library/', include('library.urls')),
    path('account/', include('account.urls')),
    path('qr', qr)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# sudo systemctl restart nginx
# sudo systemctl restart gunicorn
# sudo systemctl daemon-reload
# sudo systemctl restart gunicorn


# sudo journalctl --rotate
# sudo journalctl --vacuum-time=1s

# sudo journalctl -u gunicorn

# celery -A main beat
# celery -A main worker -l INFO --pool=solo
