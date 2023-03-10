# Generated by Django 4.1.5 on 2023-01-21 14:34

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, max_length=100, verbose_name='Nickname')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Logo')),
                ('picture', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Picture')),
                ('stars', models.PositiveSmallIntegerField(default=0, verbose_name='Number of stars')),
                ('country', models.CharField(max_length=100, verbose_name='Country')),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('street', models.CharField(blank=True, max_length=100, verbose_name='Street')),
                ('building', models.CharField(max_length=20, verbose_name='Building')),
                ('address_details', models.CharField(blank=True, max_length=100, verbose_name='Address details')),
                ('zip_code', models.CharField(max_length=20, verbose_name='Zip code')),
                ('longitude', models.DecimalField(blank=True, decimal_places=15, max_digits=20, null=True, verbose_name='Longitude')),
                ('latitude', models.DecimalField(blank=True, decimal_places=15, max_digits=20, null=True, verbose_name='Latitude')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None, verbose_name='Phone number')),
                ('site', models.URLField(blank=True, max_length=100, verbose_name='Site URL')),
            ],
            options={
                'verbose_name': 'restaurant',
                'verbose_name_plural': 'restaurants',
                'db_table': 'restaurants_restaurant',
                'ordering': ['pk'],
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RestaurantCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'restaurant category',
                'verbose_name_plural': 'restaurant categories',
                'db_table': 'restaurants_restaurantcategory',
                'ordering': ['pk'],
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RestaurantCategoryTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=100, verbose_name='Category name')),
            ],
            options={
                'verbose_name': 'restaurant category Translation',
                'db_table': 'restaurants_restaurantcategory_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RestaurantTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('name', models.CharField(max_length=100, verbose_name='Restaurant name')),
                ('description', models.TextField(blank=True, max_length=5000, verbose_name='Restaurant description')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='restaurants.restaurant')),
            ],
            options={
                'verbose_name': 'restaurant Translation',
                'db_table': 'restaurants_restaurant_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='RestaurantStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(choices=[('owner', 'Restaurant owner'), ('worker', 'Restaurant worker')], max_length=25, verbose_name='Position')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant_staff', to='restaurants.restaurant', verbose_name='Restaurant')),
            ],
            options={
                'verbose_name': 'restaurant ownerships or employments',
                'db_table': 'restaurants_restaurantstaff',
                'ordering': ['pk'],
            },
        ),
    ]
