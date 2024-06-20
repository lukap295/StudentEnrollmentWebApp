# Generated by Django 5.0.6 on 2024-06-03 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0016_alter_user_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'administrator'), ('prof', 'profesor'), ('stu', 'student')], default='stu', max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('none', 'None'), ('izv', 'izvanredni student'), ('red', 'redovni student')], default='none', max_length=20),
        ),
    ]
