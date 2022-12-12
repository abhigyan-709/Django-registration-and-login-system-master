from django.urls import path
from .views import home, profile, RegisterView
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('equipments', views.EquipmentDetails, name='equipments'),
    path('dataframe', views.ProcessData, name='dataframe'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
]
