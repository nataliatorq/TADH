# Generated by Django 5.1.2 on 2024-10-18 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jogos', '0004_alter_baseuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseuser',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
