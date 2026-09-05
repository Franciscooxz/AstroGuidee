from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.services_index, name='index'),
    path('<slug:slug>/', views.service_detail, name='detail'),
]
