from django.db import migrations
from django.utils.text import slugify


def populate_slugs(apps, schema_editor):
    Service = apps.get_model('services', 'Service')
    used = set(Service.objects.exclude(slug=None).values_list('slug', flat=True))
    for service in Service.objects.filter(slug=None):
        base = slugify(service.title) or 'servicio'
        slug = base
        counter = 1
        while slug in used:
            slug = f'{base}-{counter}'
            counter += 1
        used.add(slug)
        service.slug = slug
        service.save(update_fields=['slug'])


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_service_slug'),
    ]

    operations = [
        migrations.RunPython(populate_slugs, migrations.RunPython.noop),
    ]
