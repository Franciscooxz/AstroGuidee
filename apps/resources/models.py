from django.db import models
from django.utils.text import slugify


class ResourceCategory(models.Model):
    slug = models.SlugField(max_length=60, unique=True, blank=True)
    title = models.CharField(max_length=200)
    intro = models.TextField(blank=True)
    icon = models.CharField(max_length=80, default='fa-book')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = 'Categoria de Recursos'
        verbose_name_plural = 'Categorias de Recursos'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or 'categoria'
            slug = base
            counter = 1
            while ResourceCategory.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Resource(models.Model):
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=300)
    content = models.TextField()
    image = models.ImageField(upload_to='resources/', blank=True, null=True)
    file = models.FileField(upload_to='resources/pdf/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'

    def __str__(self):
        return self.title
