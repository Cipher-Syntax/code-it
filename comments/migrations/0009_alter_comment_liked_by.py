# Generated by Django 5.2.1 on 2025-06-14 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0008_rename_likes_comment_liked_by'),
        ('posts', '0009_remove_posts_comments_remove_posts_likes_posts_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='liked_by',
            field=models.ManyToManyField(blank=True, related_name='liked_comments', to='posts.posts'),
        ),
    ]
