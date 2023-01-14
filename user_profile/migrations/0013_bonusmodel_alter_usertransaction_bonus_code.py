# Generated by Django 4.1.3 on 2023-01-14 02:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0012_g2fa'),
    ]

    operations = [
        migrations.CreateModel(
            name='BonusModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('amount', models.FloatField(verbose_name='Amount')),
                ('first_deposit_bonus', models.IntegerField(default=0, verbose_name='First Deposit Bonus (%)')),
                ('activation_msg', models.TextField(default='Your PROMO-CODE has been succesfully activated!', verbose_name='Text After Activation')),
                ('global_ban', models.BooleanField(default=False, verbose_name='Global Ban')),
                ('trading_ban', models.BooleanField(default=False, verbose_name='Trading Ban')),
                ('support_ban', models.BooleanField(default=False, verbose_name='Support Ban')),
                ('chat_ban', models.BooleanField(default=False, verbose_name='Chat Ban')),
                ('token', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.token', verbose_name='Token')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Bonus',
                'verbose_name_plural': 'Bonuses',
            },
        ),
        migrations.AlterField(
            model_name='usertransaction',
            name='bonus_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_profile.bonusmodel'),
        ),
    ]
