# Generated by Django 5.1.4 on 2025-02-08 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Predictivehealthapp', '0013_chathistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='slottable',
            name='token',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
