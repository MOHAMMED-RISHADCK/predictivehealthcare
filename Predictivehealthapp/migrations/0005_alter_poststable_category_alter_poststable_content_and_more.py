# Generated by Django 5.1.4 on 2024-12-24 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Predictivehealthapp', '0004_rename_file_poststable_filepost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poststable',
            name='category',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='poststable',
            name='content',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='poststable',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
