import time
import uuid
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, Interest, Like, Bookmark
from itertools import chain
import random
import ast
from django.conf import settings as conf_settings
from django.core.mail import send_mail
from smtplib import SMTPException
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import datetime
from datetime import datetime
from datetime import date
from datetime import timedelta
import os



@login_required(login_url='signin')
def upload(request):
    if request.method == 'POST':
        user = request.user.username
        property_image = request.FILES.get('image_upload')
        price = request.POST['price']
        area = request.POST['area']
        location = request.POST['location']
        property_type = request.POST['property_type']
        property_image_flag = False

        if request.FILES.get('property_image') != None:
            property_image = request.FILES.get('property_image')
            property_image_flag = True

        if price == 0:
            messages.info(request, 'Please enter price and price not be 0')
            return redirect('/user/addpost')
        elif area == 0:
            messages.info(request, 'Please enter area and area not be 0')
            return redirect('/user/addpost')
        elif len(location)==0:
            messages.info(request, 'Please enter location')
            return redirect('/user/addpost')
        elif len(property_type)==0:
            messages.info(request, 'Please enter (property type')
            return redirect('/user/addpost')
        else:
            new_post = Post.objects.create(user=user,area=area, location=location, property_type=property_type,
                                       price=price)
            new_post.save()
            if property_image_flag :
                new_post.property_image = property_image
            new_post.save()

            return redirect('/')
    else:
        return redirect('/')


def search(request):
    if request.method == 'POST':
        location = request.POST['location']
        post_object = Post.objects.filter(location__icontains=location)

        post_list = []

        for ids in post_object:
            post = Post.objects.get(id=ids.id)
            post_list.append(post)


        return render(request, 'search.html',
                  {'post_list': post_list})

'''@login_required(login_url='signin')
def support(request):
    return render(request, 'support.html')
'''

def home(request):
    if not request.user.is_anonymous:
        user_object = User.objects.get(username=request.user.username)
        user = Profile.objects.get(user=user_object)
        post_list = Post.objects.filter(user=user.user)

        return render(request, 'home.html', {
        'user':user,
        'post_list': post_list})

    return render(request, 'home.html')


@login_required(login_url='userSignin')
def myList(request):
    bookmarks = Bookmark.objects.filter(id_user=request.user.id)
    bookmarks_post_list = []
    for bookmark in bookmarks:
        post_object = Post.objects.get(id=bookmark.id_post)
        bookmarks_post_list.append(post_object)

    likes = Like.objects.filter(id_user=request.user.id)
    likes_post_list = []
    for like in likes:
        post_object = Post.objects.get(id=like.id_post)
        likes_post_list.append(post_object)
    return render(request, 'mylist.html',
                  {'bookmarks_post_list': bookmarks_post_list, 'likes_post_list': likes_post_list})


'''def aboutus(request):
    return render(request, 'aboutus.html')

def joinus(request):
    return render(request, 'joinus.html')
'''

@login_required(login_url='signin')
def post(request, postid):
    post = Post.objects.get(id=postid)  # post id
    user_object = User.objects.get(username=post.user)
    post_user = Profile.objects.get(user=user_object)

    post.no_of_views = post.no_of_views + 1
    post.save()

    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user)

    bookmark = False
    like = False

    if Bookmark.objects.filter(id_user=request.user.id,id_post=postid).first():
        bookmark = True
    else:
        bookmark = False
    if Like.objects.filter(id_user=request.user.id, id_post=postid).first():
        like = True
    else:
        like = False


    return render(request, 'post.html',{'post_user':post_user,'like' : like,'bookmark':bookmark,
                  'postid': postid, 'post': post, 'profile': profile})

@login_required(login_url='signin')
def interest(request):
    if request.method == 'POST':
        postid = request.POST['postid']
        user = request.POST['user']
        post_user = request.POST['post_user']
        user_object1 = User.objects.get(username=user)
        user_profile = Profile.objects.get(user=user_object1)
        user_object2 = User.objects.get(username=post_user)
        post_user_profile = Profile.objects.get(user=user_object2)

        interest_obj = Interest.objects.create(id_user= user_profile.id_user, id_post=postid)
        interest_obj.save()

        try:
            subject = f'From Rentify '
            message = f'Seller details \n  name : {post_user_profile.user}  \n phone {post_user_profile.phone} \n email {post_user_profile.email}  Date & Time : {datetime.now()}.'
            email_from = conf_settings.EMAIL_HOST_USER
            recipient_list = [user_profile.email, ]
            send_mail(subject, message, email_from, recipient_list)
        except SMTPException as e:
            pass
        except:
            pass

        try:
            subject = f'From Rentify '
            message = f'buyer details \n name : {user_profile.user}  \n phone {user_profile.phone} \n email {user_profile.email}  Date & Time : {datetime.now()}.'
            email_from = conf_settings.EMAIL_HOST_USER
            recipient_list = [post_user_profile.email, ]
            send_mail(subject, message, email_from, recipient_list)
        except SMTPException as e:
            pass
        except:
            pass
        return redirect('/post/' + postid)

    return redirect('/')


@login_required(login_url='signin')
def deletePost(request, postid):
    post = Post.objects.get(id=postid)  # post id

    Bookmark.objects.filter(id_post=post.id).delete()
    Like.objects.filter(id_post=post.id).delete()
    Interest.objects.filter(id_post=post.id).delete()

    post.delete()
    return redirect('/')



@login_required(login_url='signin')
def addPost(request):
    return render(request, 'addpost.html')



@login_required(login_url = 'signin')
def bookmark(request):
    if request.method == 'POST':
        postid = request.POST['postid']
        if request.user.first_name != "":
            if Bookmark.objects.filter(id_user = request.user.id, id_post = postid).first():
                bookmark_object = Bookmark.objects.get(id_user = request.user.id, id_post = postid)
                bookmark_object.delete()
                return redirect('/post/' + postid)
            else:
                bookmark_object = Bookmark.objects.create(id_user = request.user.id, id_post = postid)
                bookmark_object.save()
                return redirect('/post/' + postid)
        return redirect('/post/' + postid)
    return redirect('/')

@login_required(login_url = 'signin')
def like(request):
    if request.method == 'POST':
        postid = request.POST['postid']
        if request.user.first_name != "":
            if Like.objects.filter(id_user = request.user.id, id_post = postid).first():
                like_object = Like.objects.get(id_user = request.user.id, id_post = postid)
                like_object.delete()

                post = Post.objects.get(id=postid)
                post.no_of_likes =post.no_of_likes - 1
                post.save()
                return redirect('/post/' + postid)
            else:
                like_object = Like.objects.create(id_user = request.user.id, id_post = postid)
                like_object.save()

                post = Post.objects.get(id=postid)
                post.no_of_likes = post.no_of_likes + 1
                post.save()
                return redirect('/post/' +postid)
        return redirect('/post/' + postid)
    return redirect('/')



def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        phone = request.POST['phone']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('/user/signup')

            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('/user/signup')

            elif len(phone) != 10:
                messages.info(request, 'Phone number only contain 10 digit')
                return redirect('/user/signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password, first_name = firstname, last_name = lastname)
                user.save()


                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)


                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id, phone = phone, email = email)
                new_profile.save()
                return redirect('/')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('/user/signup')

    else:
        return render(request, 'signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('/user/signin')

    else:
        return render(request, 'signin.html')


@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('/user/signin')
