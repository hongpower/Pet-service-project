"""pet_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('get_gu/', views.getGu, name='getGu'),
    path('get_business/', views.getBusiness),
    path('get_info/', views.getInfo),
    path('index2/', views.index2),
    path('get_map/',views.Map),
    path('score/', views.score),
    path('getscore/', views.getScore),
    path('getpie/', views.getPie),
    # path(),
    # path('draw_map/',views.drawMap),
    # path('get_map/', views.),
]
