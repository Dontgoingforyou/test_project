from django.urls import path
from menu import views
from menu.apps import MenuConfig

app_name = MenuConfig.name

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]