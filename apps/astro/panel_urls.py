from django.urls import path
from . import panel_views as views

app_name = 'gestion'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('estadisticas/', views.stats, name='stats'),
    path('anuncios/', views.announcements, name='announcements'),

    path('unidades/', views.units, name='units'),
    path('unidades/nueva/', views.unit_edit, name='unit_new'),
    path('unidades/<int:pk>/editar/', views.unit_edit, name='unit_edit'),
    path('unidades/<int:pk>/eliminar/', views.unit_delete, name='unit_delete'),

    path('lecciones/', views.lessons, name='lessons'),
    path('lecciones/nueva/', views.lesson_edit, name='lesson_new'),
    path('lecciones/<int:pk>/editar/', views.lesson_edit, name='lesson_edit'),
    path('lecciones/<int:pk>/eliminar/', views.lesson_delete, name='lesson_delete'),

    path('tarjetas/', views.cards, name='cards'),
    path('tarjetas/nueva/', views.card_edit, name='card_new'),
    path('tarjetas/<int:pk>/editar/', views.card_edit, name='card_edit'),
    path('tarjetas/<int:pk>/eliminar/', views.card_delete, name='card_delete'),

    path('quizzes/', views.questions, name='questions'),
    path('quizzes/nueva/', views.question_edit, name='question_new'),
    path('quizzes/<int:pk>/editar/', views.question_edit, name='question_edit'),
    path('quizzes/<int:pk>/eliminar/', views.question_delete, name='question_delete'),

    path('tienda/', views.shop, name='shop'),
    path('tienda/nuevo/', views.shop_edit, name='shop_new'),
    path('tienda/<int:pk>/editar/', views.shop_edit, name='shop_edit'),
    path('tienda/<int:pk>/eliminar/', views.shop_delete, name='shop_delete'),

    path('logros/', views.achievements, name='achievements'),
    path('logros/nuevo/', views.achievement_edit, name='achievement_new'),
    path('logros/<int:pk>/editar/', views.achievement_edit, name='achievement_edit'),
    path('logros/<int:pk>/eliminar/', views.achievement_delete, name='achievement_delete'),
]
