# Generated by Django 5.1.4 on 2025-01-02 08:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Predictivehealthapp', '0007_merge_20250102_0048'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usertable',
            old_name='city',
            new_name='gender',
        ),
        migrations.AddField(
            model_name='usertable',
            name='password',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bookinginfotable',
            name='DOCTORID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Predictivehealthapp.doctortable'),
        ),
        migrations.AlterField(
            model_name='reviewtable',
            name='DOCTORID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='DOCTORID', to='Predictivehealthapp.doctortable'),
        ),
    ]
