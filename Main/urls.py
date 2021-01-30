"""Tasklist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from . import views as v

urlpatterns = [
    path('', v.login_user, name='login'),
    path('signup/', v.signup, name='signup'),
    path('delete/<task_id>', v.delete_task, name='delete_task'),
    path('update/<task_id>', v.update_task, name='update_task'),
    path('set/<task_id>', v.set_task, name='set_task'),
]
