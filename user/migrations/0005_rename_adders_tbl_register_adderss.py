# Generated by Django 5.1.1 on 2024-09-25 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_tbl_product_quantity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tbl_register',
            old_name='adders',
            new_name='adderss',
        ),
    ]
