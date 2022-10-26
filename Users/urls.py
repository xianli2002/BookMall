from . import views
from django.urls import path

urlpatterns = [
    path('usernames/<username:username>/count/',views.usernameCountAPI.as_view()),
    path('register/new/',views.registerNewAPI.as_view()),
    path('mobiles/<phonenumber>/count/',views.mobileCountAPI.as_view()),
    path('login/userlogin/',views.userloginAPI.as_view()),
    path('logout/',views.logoutAPI.as_view()),
    path('info/',views.centerViewAPI.as_view()),
    path('password/',views.passwordChangeAPI.as_view()),
    path('browse_histories/',views.UserHistoryView.as_view()),
]