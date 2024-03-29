# Generated by Django 4.1.3 on 2022-12-12 18:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        ('user_profile', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='bonusmodel',
            name='token',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.token', verbose_name='Token'),
        ),
        migrations.AddField(
            model_name='bonusmodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.CreateModel(
            name='ExtendenBonusModel',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('main.bonusmodel',),
        ),
    ]
