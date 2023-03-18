
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='bank-home'),

    path('about/', views.about, name='bank-about'),
    path('login/', views.login, name='bank-login'),
    path('signup', views.signup, name='bank-signup'),

]