# Generated by Django 5.1.1 on 2024-09-26 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_rename_adderss_tbl_register_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='tbl_booktable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('email', models.EmailField(max_length=50, null=True)),
                ('mobile', models.CharField(max_length=20, null=True)),
                ('no_of_people', models.IntegerField(null=True)),
                ('date_of_booking', models.CharField(max_length=200, null=True)),
                ('time_of_booking', models.CharField(max_length=30, null=True)),
                ('type_of_event', models.CharField(max_length=50, null=True)),
                ('type_of_food', models.CharField(max_length=40, null=True)),
                ('booking_date', models.DateField(null=True)),
            ],
        ),
    ]
