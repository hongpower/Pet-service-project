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
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.mainpage),
    path('index/', views.index, name='index'),
    path('get_gu/', views.getGu, name='getGu'),
    path('get_business/', views.getBusiness),
    path('get_info/', views.getInfo),
    path('get_map/',views.Map),
    path('score/', views.score),
    path('getbargraph/', views.getBargraph),
    path('Geo/',views.Geo),
    path("score/get_myloc/",views.my_loc),
    path("media/", views.media),
    path('menu/',views.menu),
    path('menu/get_myloc/',views.my_loc),
    path('get_score/',views.load_score),
    path('get_rank/',views.load_rank),
    path('click_bs/',views.click_bs),
]
urlpatterns += \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)