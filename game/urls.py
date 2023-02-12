from django.urls import path
from game import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('get_trajectory_data', views.get_trajectory_data, name='get_trajectory_data'),

    ]

