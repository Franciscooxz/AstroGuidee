from django.contrib import admin
from .models import SiteConfig, HomeSection, AboutPage, Founder

@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'email', 'whatsapp']

@admin.register(HomeSection)
class HomeSectionAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ['__str__']

@admin.register(Founder)
class FounderAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'is_active', 'order']
    list_editable = ['is_active', 'order']
