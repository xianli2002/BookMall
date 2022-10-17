from django.urls import path
from . import views

urlpatterns = [
    path('areas/',views.ProvinceGetAPIView.as_view()),
    path('areas/<id>/',views.AreaGetAPIView.as_view()),
    path('addresses/create/',views.AddressAPIView.as_view()),
    path('addresses/',views.AddressAPIView.as_view()),
    path('addresses/<id>/',views.AddressAPIView.as_view()),
    path('addresses/<id>/title/',views.TitleUpdateAPIView.as_view()),
]