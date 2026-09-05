from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='year',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
