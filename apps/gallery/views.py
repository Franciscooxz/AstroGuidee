from django.shortcuts import render, get_object_or_404
from .models import Album


def gallery_index(request):
    albums = Album.objects.filter(is_active=True)
    return render(request, 'galeria/index.html', {
        'albums': albums,
        'active_nav': 'galeria',
    })


def album_detail(request, pk):
    album = get_object_or_404(Album, pk=pk, is_active=True)
    photos = album.photos.all()
    return render(request, 'galeria/album.html', {
        'album': album,
        'photos': photos,
        'active_nav': 'galeria',
    })
