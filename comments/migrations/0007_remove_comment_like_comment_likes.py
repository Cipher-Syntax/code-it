# Generated by Django 5.2.1 on 2025-06-14 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0006_alter_notifications_from_user_and_more'),
        ('users', '0002_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='like',
        ),
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_comments', to='users.userregistration'),
        ),
    ]
