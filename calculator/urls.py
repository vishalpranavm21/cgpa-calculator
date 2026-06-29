from django.urls import path
from . import views

urlpatterns = [
    path('',          views.home,          name='home'),
    path('api/health/',    views.health_check,  name='health'),
    path('api/grades/',    views.grade_criteria, name='grades'),
    path('api/calculate/', views.calculate_cgpa, name='calculate'),
]
