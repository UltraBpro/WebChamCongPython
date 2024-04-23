import sqlite3
from math import sin, cos, sqrt, atan2, radians
from django.shortcuts import render
from .models import Account
from geopy.geocoders import Nominatim
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
def authenticate(username, password):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    c.execute("SELECT * FROM WebChamCong_Account WHERE username=? AND password=?", (username, password))
    row = c.fetchone()
    conn.close()
    if row:
        return True
    return False
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if authenticate(username=username, password=password):
            return HttpResponseRedirect('/main/')  # Chuyển hướng đến trang main.html sau khi đăng nhập thành công
        else:
            error_message = "Sai tên đăng nhập hoặc mật khẩu."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def main_view(request):
    return render(request, 'main.html')


def distance_between_points(lat1, lon1, lat2, lon2):
    # Đổi đơn vị từ độ sang radian
    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(lat2)
    lon2 = radians(lon2)
    # Bán kính trung bình của trái đất (đơn vị: km)
    R = 6371.0
    # Tính độ chênh lệch giữa vĩ độ và kinh độ của hai điểm
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    # Sử dụng công thức Haversine để tính khoảng cách giữa hai điểm
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    return distance
def calculate_distance_view(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    # giả sử vị trí cố định là (10, 10)
    distance = distance_between_points(lat, lon, 10, 10)
    return HttpResponse(str(distance))