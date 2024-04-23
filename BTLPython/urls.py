from django.urls import path
from WebChamCong import views
urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('main/', views.main_view, name='main'),
    path('calculate_distance_view', views.calculate_distance_view, name='calculate_distance_view'),
]
