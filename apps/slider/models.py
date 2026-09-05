from django.db import models


class Slide(models.Model):
    image = models.ImageField(upload_to='slider/')
    title = models.CharField(max_length=200, blank=True, default='')
    subtitle = models.CharField(max_length=300, blank=True)
    link_url = models.CharField(max_length=500, blank=True)
    link_text = models.CharField(max_length=100, blank=True, default='Ver mas')
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Slide'
        verbose_name_plural = 'Slides del Slider'

    def __str__(self):
        return self.title or f'Slide #{self.order}'
