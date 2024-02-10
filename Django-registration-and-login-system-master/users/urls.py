from django.urls import path
from .views import home, profile, RegisterView
from . import views
from .views import home, respond_to_question
from .views import respond_to_question, response_summary


urlpatterns = [
    path('', home, name='home'),
    # path('equipments', views.EquipmentDetails, name='equipments'),
    # path('dataframe', views.ProcessData, name='dataframe'),
    # path('plot', views.plotData, name='plot'),
    path('register/', RegisterView.as_view(), name='users-register'),
    path('profile/', profile, name='users-profile'),
    path('respond-to-question/', respond_to_question, name='respond_to_question'),
    path('response-summary/', response_summary, name='response-summary'),
]
