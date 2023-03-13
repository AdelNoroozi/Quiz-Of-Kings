# Generated by Django 4.1.7 on 2023-03-12 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_question_dislikes_question_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='modificated_at',
            new_name='modified_at',
        ),
        migrations.AlterField(
            model_name='match',
            name='joining_player_score',
            field=models.PositiveIntegerField(default=0, verbose_name='joining player score'),
        ),
        migrations.AlterField(
            model_name='match',
            name='starter_player_score',
            field=models.PositiveIntegerField(default=0, verbose_name='starter player score'),
        ),
    ]
