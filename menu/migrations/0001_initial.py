# Generated by Django 5.1.1 on 2024-10-03 15:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Уникальное имя меню', max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Имя',
                'verbose_name_plural': 'Имена',
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Название пункта меню', max_length=100)),
                ('url', models.CharField(help_text='URL', max_length=200)),
                ('order', models.PositiveIntegerField(default=0, help_text='Порядок отображения')),
                ('menu', models.ForeignKey(help_text='Название меню', on_delete=django.db.models.deletion.CASCADE, related_name='items', to='menu.menu')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='menu.menuitem')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]
