"""mysite URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from . import views

# 规定网站,启动本地服务器,路由
urlpatterns = [
    path('admin/', admin.site.urls),  # 用户名、密码
    path('', views.home, name='home'),
    path('blog/', include('blog.urls')),  # blog APP子路由
    path('ckeditor', include('ckeditor_uploader.urls')),  # ckeditor url设置
    path('comment/', include('comment.urls')),
    path('likes/', include('likes.urls')),
    path('user/', include('user.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)