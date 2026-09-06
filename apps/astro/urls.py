from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import views

app_name = 'astro'

urlpatterns = [
    path('', views.home, name='home'),

    # Autenticacion
    path('registro/', views.register, name='register'),
    path('entrar/', views.login_view, name='login'),
    path('salir/', views.logout_view, name='logout'),

    # Recuperar contraseña
    path('recuperar/', auth_views.PasswordResetView.as_view(
        template_name='astro/auth/pw_reset.html',
        email_template_name='astro/auth/pw_reset_email.html',
        subject_template_name='astro/auth/pw_reset_subject.txt',
        success_url=reverse_lazy('astro:password_reset_done'),
    ), name='password_reset'),
    path('recuperar/enviado/', auth_views.PasswordResetDoneView.as_view(
        template_name='astro/auth/pw_reset_done.html',
    ), name='password_reset_done'),
    path('restablecer/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='astro/auth/pw_reset_confirm.html',
        success_url=reverse_lazy('astro:password_reset_complete'),
    ), name='password_reset_confirm'),
    path('restablecer/listo/', auth_views.PasswordResetCompleteView.as_view(
        template_name='astro/auth/pw_reset_complete.html',
    ), name='password_reset_complete'),

    # App (requiere sesion)
    path('app/', views.ruta, name='ruta'),
    path('app/bienvenida/', views.onboarding, name='onboarding'),
    path('app/certificado/<slug:slug>/', views.certificate, name='certificate'),
    path('app/unidad/<slug:slug>/examen/', views.exam, name='exam'),
    path('app/unidad/<slug:slug>/examen/finalizar/', views.finish_exam, name='finish_exam'),
    path('app/perfil/', views.profile, name='profile'),
    path('app/estadisticas/', views.stats, name='stats'),
    path('app/ajustes/', views.settings_view, name='settings'),
    path('app/ligas/', views.league, name='league'),
    path('app/explorar/', views.glossary, name='glossary'),
    path('app/misiones/', views.missions, name='missions'),
    path('app/misiones/reclamar/<slug:key>/', views.claim_mission, name='claim_mission'),
    path('app/cofre/abrir/', views.open_chest, name='open_chest'),
    path('app/notificaciones/', views.notifications, name='notifications'),
    path('app/notificaciones/borrar/', views.clear_notifications, name='clear_notifications'),
    path('app/repaso/', views.review, name='review'),
    path('app/repaso/flojos/', views.review_weak, name='review_weak'),
    path('app/repaso/finalizar/', views.finish_review, name='finish_review'),
    path('app/reportar/<int:qid>/', views.report_question, name='report_question'),
    path('app/tienda/', views.store, name='store'),
    path('app/tienda/comprar/<slug:key>/', views.buy_item, name='buy_item'),
    path('app/tienda/equipar/<slug:key>/', views.equip_frame, name='equip_frame'),
    path('app/leccion/<slug:slug>/', views.lesson, name='lesson'),
    path('app/leccion/<slug:slug>/completar/', views.complete_lesson, name='complete_lesson'),
    path('app/leccion/<slug:slug>/quiz/', views.quiz, name='quiz'),
    path('app/leccion/<slug:slug>/quiz/finalizar/', views.finish_quiz, name='finish_quiz'),
]
