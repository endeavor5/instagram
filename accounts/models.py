from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    nickname = models.CharField(max_length=40, blank=True)
    image = models.ImageField(blank=True, null=True)
    
    # blank = True 빈 스트링을 받겠다.
    # null => 아무것도 안받겠다. 


class User(AbstractUser):
    # 더 이상 contrib.models.Model 의 user가 아니라 
    # accounts app 에 있는 user이다.
    
    # related_name => 목적어
    # 자기를 참조
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followings")
    

    