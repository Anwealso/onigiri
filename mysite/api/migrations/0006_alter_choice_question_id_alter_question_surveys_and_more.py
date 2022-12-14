# Generated by Django 4.1 on 2022-10-01 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_choice_question_result_delete_hero_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='question_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='api.question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='surveys',
            field=models.ManyToManyField(related_name='questions', to='api.survey'),
        ),
        migrations.AlterField(
            model_name='question',
            name='text',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='result',
            name='sub_time',
            field=models.DateTimeField(),
        ),
    ]
