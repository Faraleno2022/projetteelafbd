# Generated by Django 5.1.6 on 2025-04-15 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='active',
        ),
        migrations.RemoveField(
            model_name='member',
            name='hire_date',
        ),
        migrations.RemoveField(
            model_name='member',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='member',
            name='role',
        ),
        migrations.RemoveField(
            model_name='member',
            name='specialization',
        ),
        migrations.AlterField(
            model_name='member',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
