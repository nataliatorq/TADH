# Generated by Django 5.1.2 on 2024-12-07 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jogos', '0011_baseuser_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='photo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='media/'),
        ),
    ]
