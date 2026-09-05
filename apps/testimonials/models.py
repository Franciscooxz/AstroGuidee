from django.db import models


class Testimonial(models.Model):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150, blank=True)
    quote = models.TextField()
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    event = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Testimonio'
        verbose_name_plural = 'Testimonios'

    def __str__(self):
        return '{} - {}'.format(self.name, self.event or 'Testimonio')
