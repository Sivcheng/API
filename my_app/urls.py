from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('students/', views.student_list, name='student_list'), 
    path('submit/', views.submit_registration, name='submit_registration'),
    path('get-locations/', views.get_locations, name='get_locations'),
]