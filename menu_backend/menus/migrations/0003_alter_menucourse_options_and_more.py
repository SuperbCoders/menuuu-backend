# Generated by Django 4.1.5 on 2023-01-19 18:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menucourse',
            options={'ordering': ['pk'], 'verbose_name': 'course', 'verbose_name_plural': 'courses'},
        ),
        migrations.AlterModelOptions(
            name='menucoursetranslation',
            options={'default_permissions': (), 'managed': True, 'verbose_name': 'course Translation'},
        ),
    ]