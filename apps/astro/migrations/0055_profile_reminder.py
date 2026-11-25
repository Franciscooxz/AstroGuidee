from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("astro", "0054_card_accents"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="reminder_on",
            field=models.BooleanField(default=True, verbose_name="Aviso diario"),
        ),
        migrations.AddField(
            model_name="profile",
            name="reminder_hour",
            field=models.PositiveSmallIntegerField(default=19, verbose_name="Hora del aviso"),
        ),
        migrations.AddField(
            model_name="profile",
            name="last_reminded",
            field=models.DateField(blank=True, null=True, verbose_name="Ultimo aviso"),
        ),
    ]
