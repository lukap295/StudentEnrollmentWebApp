# Generated by Django 5.0.6 on 2024-06-03 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0013_uloge_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'administrator'), ('prof', 'profesor'), ('stu', 'student')], default='stu', max_length=20),
        ),
        migrations.DeleteModel(
            name='Uloge',
        ),
    ]