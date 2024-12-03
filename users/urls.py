from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import UserCreateAPIView, PaymentListCreateAPIView, PaymentRetrieveUpdateDestroyAPIView, \
    PaymentStatusAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('payment/', PaymentListCreateAPIView.as_view(), name='payment-list-create'),
    path('payment/<int:pk>/', PaymentRetrieveUpdateDestroyAPIView.as_view(), name='payment-detail'),
    path('payment/status/<str:session_id>/', PaymentStatusAPIView.as_view(), name='payment-status'),
]
