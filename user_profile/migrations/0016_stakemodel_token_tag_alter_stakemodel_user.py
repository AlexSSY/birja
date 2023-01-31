# Generated by Django 4.1.3 on 2023-01-31 15:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0015_alter_siteparameter_key_stakemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='stakemodel',
            name='token_tag',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Token Tag'),
        ),
        migrations.AlterField(
            model_name='stakemodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
