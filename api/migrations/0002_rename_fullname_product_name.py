# Generated by Django 4.2.3 on 2023-07-15 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='fullname',
            new_name='name',
        ),
    ]
