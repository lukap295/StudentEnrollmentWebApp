# Generated by Django 5.0.6 on 2024-06-03 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_korisnik_delete_roles_delete_student'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Korisnik',
        ),
    ]
