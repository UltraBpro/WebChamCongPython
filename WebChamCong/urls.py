from django.urls import path
from . import views
app_name = 'WebChamCong'
urlpatterns = [
    path('', views.login_view, name='login_view'),
    path('view_accounts/', views.view_accounts, name='view_accounts'),
    path('add_account/', views.add_account, name='add_account'),
    path('edit_accounts/<int:account_id>/', views.edit_accounts, name='edit_accounts'),
    path('change-password/', views.change_password, name='change_password'),
    path('delete_accounts/<int:account_id>/', views.delete_accounts, name='delete_accounts'),
    path('main/', views.main_view, name='main'),
    path('check_attendance', views.check_attendance, name='check_attendance'),
    path('check_attendance/<int:account_id>/', views.check_attendance, name='check_attendance'),
    path('set_host_pos', views.set_host_pos, name='set_host_pos'),
    path('calculate_distance_view', views.calculate_distance_view, name='calculate_distance_view'),
]
