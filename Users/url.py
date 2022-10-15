from . import views
from django.urls import path

urlpatterns = [
    path('usernames/<username:username>/count/', views.UsernameCountView.as_view()),
    path('mobiles/<phonenumber>/count/', views.MobileCountView.as_view()),
    path('register/new/', views.RegisterView.as_view()),
    path('login/userlogin/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('info/',views.InfoView.as_view()),
    path('password/',views.PasswordView.as_view()),
    path('changeinfo/',views.ChangeinfoView.as_view()),
]