# Generated by Django 5.1.4 on 2025-02-08 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Predictivehealthapp', '0012_slottable_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_query', models.TextField()),
                ('chatbot_response', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
