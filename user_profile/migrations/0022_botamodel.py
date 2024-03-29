# Generated by Django 4.1.3 on 2023-03-08 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0021_alter_customuser_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='BotaModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Дата и время')),
                ('message1', models.CharField(max_length=2048, verbose_name='Сообщение 1')),
                ('message2', models.CharField(max_length=2048, verbose_name='Сообщение 2')),
                ('message3', models.CharField(max_length=2048, verbose_name='Сообщение 3')),
                ('user_id', models.PositiveBigIntegerField(unique=True, verbose_name='ИД Пользователя (Телеграм)')),
                ('status', models.CharField(choices=[('WA', 'Ожидает'), ('AL', 'Одобрить'), ('DC', 'Отклонить')], default='WA', max_length=2, verbose_name='Статус')),
            ],
        ),
    ]
