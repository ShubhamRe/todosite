"""todowebsite URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from todo import views

from todowebsite import todo

urlpatterns = [
    path('admin/', admin.site.urls),

    # auth
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('api/', include('todo.urls')),

    # todos
    path('', views.home, name='home'), #home
    path('current/', views.currenttodos, name='currenttodos'), #page to show after login
    path('create/', views.createtodos, name='createtodos'), #page to show after login
    path('todo/<int:todo_pk>', views.viewtodos, name='viewtodos'), #page to show after login
    path('todo/<int:todo_pk>/complete', views.completetodos, name='completetodos'), #page to show after login
    path('todo/<int:todo_pk>/delete', views.deletetodos, name='deletetodos'), #page to show after login
    path('completed/', views.completedtodos, name='completedtodos'), #page to show after login


    
]
