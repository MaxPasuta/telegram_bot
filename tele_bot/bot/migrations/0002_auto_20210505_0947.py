# Generated by Django 2.2.7 on 2021-05-05 02:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fieldoflaw',
            options={'verbose_name': 'Область права', 'verbose_name_plural': 'Область права'},
        ),
        migrations.CreateModel(
            name='Regulations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255, verbose_name='Вопросы')),
                ('legal_flag', models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.PROTECT, to='bot.FieldOfLaw', verbose_name='Юридический флаг')),
            ],
            options={
                'verbose_name': 'Правила',
                'verbose_name_plural': 'Правила',
            },
        ),
    ]