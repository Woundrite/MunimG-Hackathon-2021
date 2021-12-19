from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout_user),
    path('personal_finance/', views.PersonalFinance),
    path('predict/', views.predict),
    path('schemes/', views.precautions),
    path('news/', views.news),
]
