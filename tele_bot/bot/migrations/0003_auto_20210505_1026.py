# Generated by Django 2.2.7 on 2021-05-05 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_auto_20210505_0947'),
    ]

    operations = [
        migrations.AddField(
            model_name='regulations',
            name='main_question',
            field=models.BooleanField(default=False, verbose_name='Основной вопрос'),
        ),
        migrations.CreateModel(
            name='StatementsOfClaim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.CharField(max_length=255, verbose_name='Документ')),
                ('action_algorithm', models.CharField(max_length=255, verbose_name='Алгоритм действия')),
                ('regulations', models.ManyToManyField(to='bot.Regulations')),
            ],
            options={
                'verbose_name': 'Исковые заявления',
                'verbose_name_plural': 'Исковые заявления',
            },
        ),
    ]
