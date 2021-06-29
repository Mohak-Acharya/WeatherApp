from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='weather-home'),
    path('delete/<city_name>/',views.delete, name='weather-delete')
]
