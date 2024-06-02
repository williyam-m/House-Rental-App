from django.urls import path
from . import views

urlpatterns = [
    path('post/<str:postid>', views.post, name='post'),
    path('', views.home, name='home'),
    path('user/upload', views.upload, name='upload'),
    path('user/search', views.search, name='search'),
    path('user/addpost/', views.addPost, name='addpost'),
    path('user/deletepost/<str:postid>', views.deletePost, name='deletepost'),
    path('user/bookmark', views.bookmark, name='bookmark'),
    path('user/like', views.like, name='like'),
    path('user/signup', views.signup, name='signup'),
    path('user/signin', views.signin, name='signin'),
    path('user/logout', views.logout, name='logout'),
    path('user/interest', views.interest, name='interest'),
    path('user/mylist', views.myList, name='mylist')

    #path('rentify/support', views.support, name='support'),
    #path('rentify/aboutus', views.aboutus, name='aboutus')
]