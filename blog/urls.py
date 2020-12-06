from django.contrib import admin
from django.urls import path


from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home') ,
    path('blog/', Get_Posts.as_view(), name='posts'),
    path('post/<str:slug>/', Get_Post.as_view(), name='post'),
    path('search/', Search.as_view(), name='search'),
    path('category/<str:slug>/', Post_By_Category.as_view(), name='category'),
]