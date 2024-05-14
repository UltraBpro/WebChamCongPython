from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    role = models.CharField(max_length=15, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

class HostPosition(models.Model):
    host_name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)  # Vĩ độ
    longitude = models.DecimalField(max_digits=9, decimal_places=6)  # Kinh độ
    def __str__(self):
        return self.host_name


class Timekeeping(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    check_in_time = models.TimeField()
    check_out_time = models.TimeField()
    month = models.IntegerField()
    year = models.IntegerField()
    update_at = models.DateTimeField(default=datetime.now)
    hourly_rate = models.FloatField()  # Tỉ lệ lương hàng giờ
    total_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)  # Tổng lương trong 1 ngày

    def calculate_total_salary(self):
        # Tính tổng lương trong ngày dựa trên số giờ làm việc và tỉ lệ lương hàng giờ
        hours_worked = (self.check_out_time - self.check_in_time).seconds / 3600
        self.total_salary = hours_worked * self.hourly_rate
