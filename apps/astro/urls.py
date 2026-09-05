from django.urls import path
from . import views

app_name = 'astro'

urlpatterns = [
    path('', views.home, name='home'),

    # Autenticacion
    path('registro/', views.register, name='register'),
    path('entrar/', views.login_view, name='login'),
    path('salir/', views.logout_view, name='logout'),

    # App (requiere sesion)
    path('app/', views.ruta, name='ruta'),
    path('app/perfil/', views.profile, name='profile'),
    path('app/ajustes/', views.settings_view, name='settings'),
    path('app/ligas/', views.league, name='league'),
    path('app/tienda/', views.store, name='store'),
    path('app/tienda/comprar/<slug:key>/', views.buy_item, name='buy_item'),
    path('app/leccion/<slug:slug>/', views.lesson, name='lesson'),
    path('app/leccion/<slug:slug>/completar/', views.complete_lesson, name='complete_lesson'),
    path('app/leccion/<slug:slug>/quiz/', views.quiz, name='quiz'),
    path('app/leccion/<slug:slug>/quiz/finalizar/', views.finish_quiz, name='finish_quiz'),
]
