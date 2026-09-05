from django.db import models


class SiteConfig(models.Model):
    site_name = models.CharField(max_length=100, default='Artistic Mold')
    tagline = models.CharField(max_length=200, default='Familia Artistico-Deportiva')
    logo = models.ImageField(upload_to='site/', blank=True, null=True)
    favicon = models.ImageField(upload_to='site/', blank=True, null=True)
    phone = models.CharField(max_length=20, default='+57 3102385343')
    whatsapp = models.CharField(max_length=20, default='+57 3124408712')
    email = models.EmailField(default='artisticmoldfad@gmail.com')
    instagram = models.CharField(max_length=100, default='@artisticmoldfad')
    instagram_url = models.URLField(blank=True)
    facebook = models.CharField(max_length=100, default='@ArtisticMoldFAD')
    facebook_url = models.URLField(blank=True)
    blog_section_name = models.CharField(max_length=50, default='Blog')
    address = models.CharField(max_length=300, blank=True, default='Bogota, Colombia')
    convenio = models.CharField(max_length=200, blank=True, default='Convenio 552 del 2023')

    class Meta:
        verbose_name = 'Configuracion del Sitio'
        verbose_name_plural = 'Configuracion del Sitio'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class HomeSection(models.Model):
    title = models.CharField(max_length=200, default='Quienes Somos')
    description = models.TextField(default='Artistic Mold es un Dispositivo de Base Comunitaria (DBC).')
    image_1 = models.ImageField(upload_to='home/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='home/', blank=True, null=True)
    cta_text = models.CharField(max_length=50, default='Conocenos', blank=True)
    cta_url = models.CharField(max_length=200, default='/nosotros/', blank=True)
    stat_1_number = models.CharField(max_length=20, default='10+', blank=True)
    stat_1_label = models.CharField(max_length=50, default='Cofundadores', blank=True)
    stat_2_number = models.CharField(max_length=20, default='30+', blank=True)
    stat_2_label = models.CharField(max_length=50, default='Integrantes', blank=True)
    stat_3_number = models.CharField(max_length=20, default='50+', blank=True)
    stat_3_label = models.CharField(max_length=50, default='Disciplinas', blank=True)

    class Meta:
        verbose_name = 'Seccion Principal del Home'
        verbose_name_plural = 'Seccion Principal del Home'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class AboutPage(models.Model):
    historia = models.TextField(default='', blank=True)
    mision = models.TextField(default='', blank=True)
    vision = models.TextField(default='', blank=True)
    preceptos = models.TextField(default='', blank=True)
    simbolos = models.TextField(default='', blank=True)
    frase_emblema = models.TextField(default='EL OPUESTO DE ADICCION NO ES SOBRIEDAD, ES CONEXION', blank=True)
    imagen_hero = models.ImageField(upload_to='nosotros/', blank=True, null=True)

    class Meta:
        verbose_name = 'Pagina Nosotros'
        verbose_name_plural = 'Pagina Nosotros'

    def __str__(self):
        return 'Contenido Nosotros'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Founder(models.Model):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150, blank=True)
    photo = models.ImageField(upload_to='founders/', blank=True, null=True)
    bio = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Fundador'
        verbose_name_plural = 'Fundadores'

    def __str__(self):
        return self.name


class PolicyPage(models.Model):
    content = models.TextField(default='', blank=True)
    is_active = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Politica de Privacidad'
        verbose_name_plural = 'Politica de Privacidad'

    def __str__(self):
        return 'Politica de Privacidad'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
