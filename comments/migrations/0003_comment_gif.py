# Generated by Django 5.2.1 on 2025-06-03 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_comment_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='gif',
            field=models.ImageField(blank=True, null=True, upload_to='comment_images'),
        ),
    ]
