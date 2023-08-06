from django.urls import path,include , path
from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('cupcake/list',views.cake_list,name="cake_list"),
    path('cupcake/<pk>',views.cupcake_detail,name="cupcake_detail"),
    path('cake/new', views.cake_new, name='cake_new'),
    path('newcake', views.newcake_detail, name='newcake_detail'),
    path('register', views.registerView, name='register'),
    path('', views.loginView, name='login'),
    path('logout', views.logoutView, name='logout'),
    path('customcakeView', views.customcakeView, name='customcakeView'),
]
