# Generated by Django 5.2 on 2025-04-17 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sathi', '0002_note_profile_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='file',
            field=models.FileField(upload_to='Padhai-Sathi/sathi/functions/teacher/'),
        ),
    ]
