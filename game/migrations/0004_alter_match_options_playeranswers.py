# Generated by Django 4.1.7 on 2023-03-12 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('game', '0003_alter_match_modificated_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='match',
            options={'verbose_name': 'Match', 'verbose_name_plural': 'Matches'},
        ),
        migrations.CreateModel(
            name='PlayerAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_answers', to='game.choice')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_answers', to='game.match', verbose_name='match')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='player_answers', to='accounts.player', verbose_name='player')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player_answers', to='game.question', verbose_name='question')),
            ],
            options={
                'verbose_name': 'Player Answer',
                'verbose_name_plural': 'Player Answers',
            },
        ),
    ]
