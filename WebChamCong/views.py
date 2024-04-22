import sqlite3

from django.shortcuts import render
from .models import Account

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
