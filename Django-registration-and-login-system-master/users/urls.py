from django.urls import path
from .views import home, profile, RegisterView
from . import views

urlpatterns = [
    path('', home, name='home'),
    # path('equipment', views.EquipmentDetails, name='equipment'),
    path('equipments', views.EquipmentDetails, name='equipments'),
    #path('sub', views.subtraction, name='sub'),
    #path('multi', views.multiplication, name='multi'),
    #path('div', views.division, name='div'),
    # path('matlib', views.matlib, name = "matlib"),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
]
