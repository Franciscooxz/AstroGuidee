from django.db import models


class Album(models.Model):
    title = models.CharField(max_length=200)
    year = models.PositiveIntegerField(blank=True, null=True)
    cover = models.ImageField(upload_to='gallery/covers/', blank=True, null=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-year', 'order']
        verbose_name = 'Album'
        verbose_name_plural = 'Albums'

    def __str__(self):
        return '{} ({})'.format(self.title, self.year)

    def photo_count(self):
        return self.photos.count()


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='gallery/photos/')
    caption = models.CharField(max_length=300, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'Foto'
        verbose_name_plural = 'Fotos'

    def __str__(self):
        return 'Foto en {}'.format(self.album.title)
