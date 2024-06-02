from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from datetime import date

User = get_user_model()
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.jpg')
    phone = models.BigIntegerField(blank=True)
    email=models.TextField(blank=True)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    property_image = models.ImageField(upload_to='post_images')
    price = models.IntegerField()
    area = models.TextField()
    location = models.TextField()
    property_type = models.TextField()
    no_of_bedrooms = models.IntegerField(default=1)
    no_of_bathrooms = models.IntegerField(default= 1)
    no_of_views = models.IntegerField(default=0)
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class Interest(models.Model):
    id_user = models.IntegerField()
    id_post = models.CharField(max_length=100)

class Like(models.Model):
    id_user = models.IntegerField()
    id_post = models.CharField(max_length=100)

class Bookmark(models.Model):
    id_user = models.IntegerField()
    id_post = models.CharField(max_length=100)
