from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('weekly', views.weekly, name='weekly'),
    path('stats', views.stats, name='stats'),
	path('',views.expense_week, name = 'expense_week'),
    path('send-email', views.EmailAPI.as_view()),
    path('',views.expense_month, name = 'expense_month'),
]