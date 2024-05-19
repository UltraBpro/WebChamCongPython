from django.db import models
class Account(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=20)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
class BangChamCong(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    ngay = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    luong_ngay = models.DecimalField(max_digits=10, decimal_places=2)
