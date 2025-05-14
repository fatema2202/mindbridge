"""
URL configuration for mindbridge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from accounts import views

urlpatterns = [
    path('community-forum/', views.forum_topic_list, name='forum_topic_list'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', views.home, name='home'),
    path('progress-journal/', views.progress_journal, name='progress_journal'),
    path('create-therapist/', views.create_therapist, name='create_therapist'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('reviews/', views.testimonial_page, name='reviews'),
]
