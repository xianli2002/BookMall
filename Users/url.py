from . import views
from django.urls import path

urlpatterns = [
    path('cart/', views.cart),
    path('detail/', views.detail),
    path('', views.index),
    path('list/', views.list),
    path('login/', views.login),
    path('place_order/', views.place_order),
    path('register/', views.register),
    path('user_center_info/', views.user_center_info),
    path('user_center_order/', views.user_center_order),
    path('user_center_site/', views.user_center_site),
]