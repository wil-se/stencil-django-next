from django.urls import path, include
from .views import (
    RegisterView,
    UserView,
    NonceSignRequestView,
    NonceSignatureView
    )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', RegisterView.as_view(), name='sign_up'),
    path('verify', TokenVerifyView.as_view(), name='token_verify'),
    path('user', UserView.as_view(), name='user'),
    path('nonce_sign_request', NonceSignRequestView.as_view(), name='nonce_sign_request'),
    path('nonce_sign_verify', NonceSignatureView.as_view(), name='nonce_sign_verify'),
    path('password_reset', include('django_rest_passwordreset.urls', namespace='password_reset')),
]