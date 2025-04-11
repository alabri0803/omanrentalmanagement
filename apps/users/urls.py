from django.urls import path
from django.contrib.auth import views as auth_views
from django.utils.translation import gettext_lazy as _
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        extra_context={'title': _('تسجيل الدخول')}
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]