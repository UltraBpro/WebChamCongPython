from math import sin, cos, sqrt, atan2, radians
from django.shortcuts import render, get_object_or_404, redirect
from .models import Account
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Account
from django.contrib.auth import authenticate, login

server_lat = None
server_lon = None


def view_accounts(request):
    accounts = Account.objects.all()
    return render(request, 'view_accounts.html', {'accounts': accounts})

def add_account(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        role = request.POST.get('role', None)
        salary = request.POST.get('salary', None)
        account = Account(username=username, password=password, role=role, salary=salary)
        account.save()
        return redirect('WebChamCong:view_accounts')
    return render(request, 'add_account.html')

def edit_accounts(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    if request.method == 'POST':
        account.password = request.POST.get('password')
        account.role = request.POST.get('role')
        account.salary = request.POST.get('salary')
        account.save()
        return redirect('WebChamCong:view_accounts')
    else:
        return render(request, 'edit_account.html', {'account': account})

def delete_accounts(request, account_id):
    account = get_object_or_404(Account, pk=account_id)
    account.delete()
    return redirect('WebChamCong:view_accounts')


def authenticate(username, password):
    try:
        account = Account.objects.get(username=username, password=password)
        return True
    except Account.DoesNotExist:
        return False


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if authenticate(username=username, password=password):
            return HttpResponseRedirect('main/')  # Chuyển hướng đến trang main.html sau khi đăng nhập thành công
        else:
            error_message = "Sai tên đăng nhập hoặc mật khẩu."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')


def main_view(request):
    return render(request, 'main.html')


def set_host_pos(request):
    global server_lat, server_lon
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    server_lat = lat
    server_lon = lon
    print("setted")
    print(server_lat)
    print(server_lon)
    return HttpResponse()


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
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


def calculate_distance_view(request):
    global server_lat, server_lon
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    print("before")
    print(server_lat)
    print(server_lon)
    distance = distance_between_points(lat, lon, float(server_lat), float(server_lon))
    return HttpResponse(str(distance))
