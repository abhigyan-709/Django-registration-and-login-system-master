from django.urls import path
from .views import home, profile, RegisterView
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('add', views.addition, name='add'),
    path('sub', views.subtraction, name='sub'),
    path('multi', views.multiplication, name='multi'),
    path('div', views.division, name='div'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
]
