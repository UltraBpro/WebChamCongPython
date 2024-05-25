from datetime import datetime, date
from math import sin, cos, sqrt, atan2, radians
from django.shortcuts import render, get_object_or_404, redirect
from .models import Account, BangChamCong
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Account
from django.contrib.auth import authenticate, login

from geopy.distance import geodesic

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

def change_password(request):
    if request.method == 'POST':
        username = request.session.get('logged_in_username')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        try:
            account = Account.objects.get(username=username)
        except Account.DoesNotExist:
            error_message = 'Tài khoản không tồn tại.'
            return render(request, 'change_password.html', {'error_message': error_message})
        # Kiểm tra mật khẩu cũ có đúng không
        if not old_password==account.password:
            error_message = 'Mật khẩu cũ không đúng.'
            return render(request, 'change_password.html', {'error_message': error_message})
        # Kiểm tra mật khẩu mới và xác nhận mật khẩu mới có khớp nhau không
        if new_password != confirm_password:
            error_message = 'Mật khẩu mới và xác nhận mật khẩu mới không khớp.'
            return render(request, 'change_password.html', {'error_message': error_message})
        # Cập nhật mật khẩu mới
        account.password = new_password
        account.save()
        success_message = 'Đổi mật khẩu thành công.'
        return render(request, 'change_password.html', {'success_message': success_message})
    return render(request, 'change_password.html')

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
            request.session['logged_in_username'] = Account.objects.get(username=username, password=password).username
            request.session['logged_in_role'] = Account.objects.get(username=username, password=password).role
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
    location1 = (lat1, lon1)
    location2 = (lat2, lon2)
    distance = geodesic(location1, location2).meters
    return distance


def calculate_distance_view(request):
    global server_lat, server_lon
    if server_lat==None:
        return HttpResponse("Chưa set server")
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    username = request.session['logged_in_username']
    distance = distance_between_points(lat, lon, float(server_lat), float(server_lon))
    if distance <= 30:
        diem_danh_va_tinh_luong(username)
    return HttpResponse(str(distance))


def diem_danh_va_tinh_luong(username):
    ngay_hien_tai = date.today()
    account = Account.objects.get(username=username)
    bang_cham_cong, created = BangChamCong.objects.get_or_create(account=account, ngay=ngay_hien_tai,
                                                                 defaults={'start_time': datetime.now().time()})
    if not created:
        bang_cham_cong.end_time = datetime.now().time()
        so_gio_lam_viec = (datetime.combine(date.min, bang_cham_cong.end_time) - datetime.combine(date.min,
                                                                                                  bang_cham_cong.start_time)).seconds / 3600
        luong_hien_tai = int(so_gio_lam_viec) * account.salary  # Chuyển đổi Decimal sang float

        BangChamCong.objects.filter(pk=bang_cham_cong.pk).update(end_time=bang_cham_cong.end_time,
                                                                 luong_ngay=luong_hien_tai)


def check_attendance(request, account_id=None):
        checkday = request.POST.get('checkday')
        logged_in_username = request.session.get('logged_in_username')
        logged_in_role = request.session.get('logged_in_role')
        if account_id!=None:
            account = get_object_or_404(Account, id=account_id)
            attendance_records = BangChamCong.objects.filter(account=account)
            checkday=account_id
        elif logged_in_role == 'admin':
            attendance_records = BangChamCong.objects.filter(ngay=checkday)
        else:
            account = Account.objects.get(username=logged_in_username)
            attendance_records = BangChamCong.objects.filter(account=account, ngay=checkday)
        context = {
            'attendance_records': attendance_records,
            'checkday': checkday,
        }
        print(attendance_records)
        return render(request, 'attendance.html', context)
