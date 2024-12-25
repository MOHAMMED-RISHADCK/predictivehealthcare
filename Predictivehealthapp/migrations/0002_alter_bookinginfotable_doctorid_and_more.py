# Generated by Django 5.1.4 on 2024-12-21 06:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Predictivehealthapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinginfotable',
            name='DOCTORID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctorid', to='Predictivehealthapp.doctortable'),
        ),
        migrations.AlterField(
            model_name='doctortable',
            name='email',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='reviewtable',
            name='DOCTORID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='DOCTORID', to='Predictivehealthapp.doctortable'),
        ),
    ]