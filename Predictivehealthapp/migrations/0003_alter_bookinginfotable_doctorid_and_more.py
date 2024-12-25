# Generated by Django 5.1.4 on 2024-12-21 06:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Predictivehealthapp', '0002_alter_bookinginfotable_doctorid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinginfotable',
            name='DOCTORID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctorid', to='Predictivehealthapp.logintable'),
        ),
        migrations.AlterField(
            model_name='reviewtable',
            name='DOCTORID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='DOCTORID', to='Predictivehealthapp.logintable'),
        ),
    ]
