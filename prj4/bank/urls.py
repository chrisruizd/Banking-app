
from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='bank-home'),

    path('about/', views.about, name='bank-about'),
    #path('login/', views.login_user, name='bank-login'),
    #path('logout', views.logout_user, name='bank-logout'),
    path('signup/', views.signup, name='bank-signup'),
    path('profile/', views.profile, name='bank-profile'),
    path('createAcc/', views.createAcc, name='bank-createAcc'),

    path('deposit/', views.deposit, name='bank-deposit'),
    path('withdraw/', views.withdraw, name='bank-withdraw'),
    path('transfer/', views.transfer, name='bank-transfer'),

    path('send/', views.send, name='bank-send'),
]