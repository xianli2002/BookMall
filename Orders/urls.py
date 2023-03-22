from django.urls import path
from . import views

urlpatterns = [
    path('orders/settlement/',views.OrderSettlementAPIView.as_view()),
    path('orders/commit/',views.OrderCommitAPIView.as_view()),
    path('orders/get/',views.OrderCommitAPIView.as_view()),
]