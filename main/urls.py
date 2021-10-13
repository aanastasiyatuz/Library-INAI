from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('library/', include('library.urls')),
    path('account/', include('account.urls')),
]

# sudo systemctl restart nginx
# sudo systemctl restart gunicorn
# sudo systemctl daemon-reload
# sudo systemctl restart gunicorn