# Generated by Django 4.1.3 on 2023-01-04 15:56

from django.db import migrations, models
import user_profile.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0006_fiat_p2p'),
    ]

    operations = [
        migrations.AddField(
            model_name='p2p',
            name='photo',
            field=models.ImageField(default='icon-gf02a4d118_640.png', upload_to=user_profile.models.P2P.image_path),
        ),
    ]
