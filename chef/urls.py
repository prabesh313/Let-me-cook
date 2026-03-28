from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('index/', views.index, name='index'),
    path('generate/', views.generate_recipe, name='generate'),
    path('nutrition/', views.nutrition, name='nutrition'), 
    path('chatbot/', views.chatbot, name='chatbot'),
]