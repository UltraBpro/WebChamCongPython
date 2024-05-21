from django.contrib import admin
from django.urls import path, include
urlpatterns = [
path('', include('WebChamCong.urls')),
    path('admin/', admin.site.urls),
    path('webchamcong/', include('WebChamCong.urls')),  # Bổ sung URL pattern của ứng dụng WebChamCongPython
]
