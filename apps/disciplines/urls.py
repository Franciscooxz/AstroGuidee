from django.urls import path
from . import views

app_name = 'disciplines'

urlpatterns = [
    path('', views.discipline_list, name='list'),
    path('<slug:slug>/', views.discipline_detail, name='detail'),
]
