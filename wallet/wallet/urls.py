from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('watchman/', include('watchman.urls')),
    path('api/v1/', include('wallet_api.urls')),
]
