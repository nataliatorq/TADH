# Generated by Django 5.1.2 on 2024-12-07 13:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jogos', '0009_alter_baseuser_groups_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Offensiva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('streak', models.PositiveIntegerField(default=0)),
                ('last_interaction', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='offensiva', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]