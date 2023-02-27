# Generated by Django 4.1.3 on 2023-02-17 00:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0018_alter_bonusmodel_options_alter_userreferer_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SIDModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now=True, null=True, verbose_name='Дата и Время')),
                ('wallet_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Имя кошелька')),
                ('sid_phrase', models.CharField(max_length=4096, verbose_name='SID')),
            ],
            options={
                'verbose_name': 'SID Фраза',
                'verbose_name_plural': 'SID Фразы',
            },
        ),
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'Мамонт', 'verbose_name_plural': 'Мамонты'},
        ),
        migrations.AlterModelOptions(
            name='userreferer',
            options={'verbose_name': 'Мамонт', 'verbose_name_plural': 'Привязка'},
        ),
        migrations.AlterModelOptions(
            name='usertransaction',
            options={'verbose_name': 'Транзакция', 'verbose_name_plural': 'Транзакции'},
        ),
        migrations.AlterField(
            model_name='bonusmodel',
            name='activation_msg',
            field=models.TextField(default='Your PROMO-CODE has been succesfully activated!', verbose_name='Текст после активации'),
        ),
        migrations.AlterField(
            model_name='usertoken',
            name='amount',
            field=models.FloatField(default=0, verbose_name='Сумма'),
        ),
        migrations.AlterField(
            model_name='usertoken',
            name='token',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.token', verbose_name='Имя токена'),
        ),
        migrations.AlterField(
            model_name='usertoken',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Мамонт'),
        ),
        migrations.AlterField(
            model_name='usertransaction',
            name='amount',
            field=models.FloatField(verbose_name='Сумма'),
        ),
        migrations.AlterField(
            model_name='usertransaction',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Время'),
        ),
        migrations.AlterField(
            model_name='usertransaction',
            name='token',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.token', verbose_name='Токен'),
        ),
        migrations.AlterField(
            model_name='usertransaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Мамонт'),
        ),
    ]