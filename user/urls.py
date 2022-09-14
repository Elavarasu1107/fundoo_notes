from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.UserRegistration.as_view(), name='register'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('verify/<str:token>', views.UserVerification.as_view(), name='verify'),
    path('change_password/', views.ChangePassword.as_view(), name='change_password'),
    path('forgot_password/', views.ForgotPassword.as_view(), name='forgot_password'),
    path('verify_forgot_password/<str:token>', views.VerifyForgotPassword.as_view(), name='verify_forgot_password'),
]
