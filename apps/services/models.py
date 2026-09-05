from django.db import models
from django.utils.text import slugify


class Service(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=220)
    description = models.TextField()
    icon = models.CharField(max_length=80, default='fa-star')
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or 'servicio'
            slug = base
            counter = 1
            while Service.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('services:detail', kwargs={'slug': self.slug})


class ServicePDF(models.Model):
    title = models.CharField(max_length=200, default='Catalogo de Servicios')
    file = models.FileField(upload_to='services/pdf/')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'PDF de Servicios'
        verbose_name_plural = 'PDFs de Servicios'

    def __str__(self):
        return self.title
