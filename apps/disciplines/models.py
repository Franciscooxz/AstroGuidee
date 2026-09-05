from django.db import models
from django.utils.text import slugify


class DisciplineCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=50, default='fa-star')
    color = models.CharField(max_length=7, default='#F5C518')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Categoria de Arte/Disciplina'
        verbose_name_plural = 'Categorias de Artes/Disciplinas'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Discipline(models.Model):
    category = models.ForeignKey(DisciplineCategory, on_delete=models.CASCADE, related_name='disciplines')
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True, max_length=170)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='disciplines/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['category__order', 'order', 'name']
        verbose_name = 'Arte / Disciplina'
        verbose_name_plural = 'Artes / Disciplinas'

    def __str__(self):
        return '{} - {}'.format(self.category.name, self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('disciplines:detail', kwargs={'slug': self.slug})
