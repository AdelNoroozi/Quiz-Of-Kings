# Generated by Django 4.1.7 on 2023-03-12 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_rename_playeranswers_playeranswer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='dislikes',
            field=models.IntegerField(default=0, verbose_name='dislikes'),
        ),
        migrations.AddField(
            model_name='question',
            name='likes',
            field=models.IntegerField(default=0, verbose_name='likes'),
        ),
    ]