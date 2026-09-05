from django.contrib import admin
from .models import DisciplineCategory, Discipline

@admin.register(DisciplineCategory)
class DisciplineCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'order']
    list_editable = ['order']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_featured', 'is_active', 'order']
    list_editable = ['is_featured', 'is_active', 'order']
    list_filter = ['category', 'is_featured', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
