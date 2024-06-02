from django.contrib import admin
from .models import Profile, Post, Interest, Like, Bookmark

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Interest)
admin.site.register(Like)
admin.site.register(Bookmark)