from django.urls import path
from . import panel_views as views

app_name = 'panel'

urlpatterns = [
    path('login/', views.panel_login, name='login'),
    path('logout/', views.panel_logout, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('config/', views.site_config_edit, name='site_config'),
    # Slider
    path('slider/', views.slider_list, name='slider_list'),
    path('slider/nuevo/', views.slide_create, name='slide_create'),
    path('slider/<int:pk>/editar/', views.slide_edit, name='slide_edit'),
    path('slider/<int:pk>/eliminar/', views.slide_delete, name='slide_delete'),
    # Blog
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/nuevo/', views.post_create, name='post_create'),
    path('blog/<int:pk>/editar/', views.post_edit, name='post_edit'),
    path('blog/<int:pk>/eliminar/', views.post_delete, name='post_delete'),
    # Blog Categories
    path('blog/categorias/', views.blog_categories_list, name='blog_categories_list'),
    path('blog/categorias/nueva/', views.blog_category_create, name='blog_category_create'),
    path('blog/categorias/<int:pk>/editar/', views.blog_category_edit, name='blog_category_edit'),
    path('blog/categorias/<int:pk>/eliminar/', views.blog_category_delete, name='blog_category_delete'),
    # Disciplines
    path('artes/', views.disciplines_list, name='disciplines_list'),
    path('artes/nuevo/', views.discipline_create, name='discipline_create'),
    path('artes/<int:pk>/editar/', views.discipline_edit, name='discipline_edit'),
    path('artes/<int:pk>/eliminar/', views.discipline_delete, name='discipline_delete'),
    # Discipline Categories
    path('artes/categorias/', views.discipline_categories_list, name='discipline_categories_list'),
    path('artes/categorias/nueva/', views.discipline_category_create, name='discipline_category_create'),
    path('artes/categorias/<int:pk>/editar/', views.discipline_category_edit, name='discipline_category_edit'),
    path('artes/categorias/<int:pk>/eliminar/', views.discipline_category_delete, name='discipline_category_delete'),
    # FAQ
    path('faq/', views.faq_list, name='faq_list'),
    path('faq/nuevo/', views.faq_create, name='faq_create'),
    path('faq/<int:pk>/editar/', views.faq_edit, name='faq_edit'),
    path('faq/<int:pk>/eliminar/', views.faq_delete, name='faq_delete'),
    # Testimonials
    path('testimonios/', views.testimonials_list, name='testimonials_list'),
    path('testimonios/nuevo/', views.testimonial_create, name='testimonial_create'),
    path('testimonios/<int:pk>/editar/', views.testimonial_edit, name='testimonial_edit'),
    path('testimonios/<int:pk>/eliminar/', views.testimonial_delete, name='testimonial_delete'),
    # Gallery
    path('galeria/', views.gallery_list, name='gallery_list'),
    path('galeria/nuevo/', views.album_create, name='album_create'),
    path('galeria/<int:pk>/editar/', views.album_edit, name='album_edit'),
    path('galeria/<int:pk>/eliminar/', views.album_delete, name='album_delete'),
    path('galeria/foto/<int:pk>/eliminar/', views.photo_delete, name='photo_delete'),
    # Policy
    path('politica/', views.policy_edit, name='policy_edit'),
    # Editor uploads
    path('upload/', views.editor_upload, name='editor_upload'),
    # Services
    path('servicios/', views.services_list, name='services_list'),
    path('servicios/nuevo/', views.service_create, name='service_create'),
    path('servicios/<int:pk>/editar/', views.service_edit, name='service_edit'),
    path('servicios/<int:pk>/eliminar/', views.service_delete, name='service_delete'),
    # Resources
    path('recursos/', views.resources_list, name='resources_list'),
    path('recursos/nuevo/', views.resource_create, name='resource_create'),
    path('recursos/<int:pk>/editar/', views.resource_edit, name='resource_edit'),
    path('recursos/<int:pk>/eliminar/', views.resource_delete, name='resource_delete'),
    path('recursos/categorias/nueva/', views.resource_category_create, name='resource_category_create'),
    path('recursos/categorias/<int:pk>/editar/', views.resource_category_edit, name='resource_category_edit'),
    path('recursos/categorias/<int:pk>/eliminar/', views.resource_category_delete, name='resource_category_delete'),
    # Founders
    path('fundadores/', views.founders_list, name='founders_list'),
    path('fundadores/nuevo/', views.founder_create, name='founder_create'),
    path('fundadores/<int:pk>/editar/', views.founder_edit, name='founder_edit'),
    path('fundadores/<int:pk>/eliminar/', views.founder_delete, name='founder_delete'),
]
