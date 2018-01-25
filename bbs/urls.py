"""bbs_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from bbs import views

urlpatterns = [

    path('', views.index),
    url(r'^category/(\d+)/$', views.category),
    url(r'details/(\d+)/$', views.article_detail, name='article_detail'),
    path('comment/', views.comment, name='post_comment'),
    url(r'comment_list/(\d+)/$', views.get_comments, name='get_comments'),
    url(r'new_article/$', views.new_article, name='new_article'),
    url(r'file_upload/$', views.file_upload, name='file_upload'),
    url(r'latest_article_count/$', views.get_latest_article_count, name='get_latest_article_count'),

]
