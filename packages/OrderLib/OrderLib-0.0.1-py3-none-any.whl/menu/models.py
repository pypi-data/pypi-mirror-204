from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # add any additional fields for user profile, such as profile picture or bio

class UserInfo(models.Model):
    username = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=100)

    class Meta:
        db_table = "UserInfo"

class Cupcake(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=20)
    rating = models.FloatField()
    weight = models.FloatField()
    image = models.ImageField(upload_to='images/cakes')
    writer = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    createdAt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Newcake(models.Model):
    name = models.CharField(max_length=200)
    price = models.CharField(max_length=20)
    weight = models.FloatField()
    image = models.ImageField(upload_to='images/cakes')
    writer = models.CharField(max_length=20 , null=True)
    createdAt = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = "NewCake"
        

