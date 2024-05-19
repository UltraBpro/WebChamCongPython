from django.db import models
class Account(models.Model):
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=50)
    role = models.CharField(max_length=20)
    salary = models.IntegerField(null=True)
class BangChamCong(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    ngay = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True)
    luong_ngay = models.IntegerField(null=True)
