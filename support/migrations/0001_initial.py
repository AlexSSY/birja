# Generated by Django 4.1.3 on 2022-12-15 14:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SupportMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now=True, verbose_name='Time')),
                ('message', models.TextField(verbose_name='Message')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='support_user', to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='support_worker', to=settings.AUTH_USER_MODEL, verbose_name='Worker')),
            ],
        ),
    ]