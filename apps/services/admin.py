from django.contrib import admin
from .models import Service, ServicePDF

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'icon', 'is_active', 'order']
    list_editable = ['is_active', 'order']

@admin.register(ServicePDF)
class ServicePDFAdmin(admin.ModelAdmin):
    list_display = ['title', 'updated_at']
