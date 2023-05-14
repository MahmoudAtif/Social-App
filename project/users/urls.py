from django.urls import path, include
from .views import v1
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('users', v1.UserProfileViewSet, basename='users')

urlpatterns = [
    path('sign-up/', v1.SignUpView.as_view(), name='sign-in'),
    path('sign-in/', v1.SignInView.as_view(), name='sign-up'),
    path('guest-sign-up/', v1.GuestSignUpView.as_view(), name='guest-sign-up'),
    path(
        'email-verification/',
        v1.EmailVerificationView.as_view(),
        name='email-verification'
    ),
    path(
        'resend-email-verification/',
        v1.ResendEmailVerificationView.as_view(),
        name='resend-email-verification'
    ),
    path(
        'reset-password/',
        v1.ResetPasswordView.as_view(),
        name='reset-password'
    ),
    path(
        'confirm-reset-password/',
        v1.ConfirmResetPasswordView.as_view(),
        name='confirm-reset-password'
    ),
    path(
        'change-password/',
        v1.ChangePasswordView.as_view(),
        name='change-password'
    ),
    path('logout/', v1.LogoutView.as_view(), name='logout'),
    # path('profile/', v1.UserProfileView.as_view(), name='user-profile'),
    path('', include(router.urls))

]
