from django.urls import path
from . import views

urlpatterns = [
    path('', views.MemberLogin, name='member-login'),
    path('signup/', views.SignUp, name='sign-up'),
    path('verify/', views.Verify, name='verify'),
]