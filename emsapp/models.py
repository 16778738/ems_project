from django.db import models


# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=20,unique=True)
    name = models.CharField(max_length=20)
    user_pwd = models.CharField(max_length=20)
    sex = models.CharField(max_length=10)

class Staff(models.Model):
    name = models.CharField(max_length=20)
    salary = models.IntegerField()
    age = models.IntegerField()
    head_pic = models.ImageField(upload_to="pic")
