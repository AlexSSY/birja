# Generated by Django 4.1.3 on 2023-01-04 16:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0008_alter_p2p_photo_alter_p2p_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='p2p',
            name='limit_end',
            field=models.FloatField(default=5000, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Limit (end)'),
        ),
        migrations.AlterField(
            model_name='p2p',
            name='limit_start',
            field=models.FloatField(default=50, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Limit (start)'),
        ),
    ]