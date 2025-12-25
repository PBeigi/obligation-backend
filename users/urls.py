from django.urls import path
from . import views

urlpatterns = [
    path('me/', views.me, name='user-me'),
    path('success/', views.success_page, name='success'),
]
