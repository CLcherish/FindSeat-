from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=20)
    pwd = models.CharField(max_length=20)
    uphone = models.CharField(max_length=11)


class Seat(models.Model):
    seatid = models.CharField(max_length=10)
    status = models.CharField(max_length=20,default='free')
    customername = models.CharField(max_length=20)