from django.contrib import admin
from .models import Album, Photo

class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 3

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'year', 'is_active', 'order']
    list_editable = ['is_active', 'order']
    inlines = [PhotoInline]

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['album', 'caption', 'order']
    list_filter = ['album']
