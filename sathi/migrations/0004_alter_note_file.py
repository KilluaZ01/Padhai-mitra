# Generated by Django 5.2 on 2025-04-17 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sathi', '0003_alter_note_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='file',
            field=models.FileField(upload_to='notes/'),
        ),
    ]
