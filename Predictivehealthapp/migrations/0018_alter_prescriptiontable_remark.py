# Generated by Django 5.1.4 on 2025-03-05 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Predictivehealthapp', '0017_doctortable_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prescriptiontable',
            name='remark',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
