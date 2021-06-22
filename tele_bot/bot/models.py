import os

from django.db import models


# область права
class FieldOfLaw(models.Model):
    theses = models.CharField(
        verbose_name='Тезисы',
        max_length=255)
    legal_flag = models.CharField(
        verbose_name='Юридический флаг',
        max_length=255)

    def __str__(self):
        return f'#{self.legal_flag}'

    class Meta:
        verbose_name = 'Область права'
        verbose_name_plural = 'Область права'


# правила
class Regulations(models.Model):
    question = models.CharField(
        verbose_name='Вопросы',
        max_length=255)
    legal_flag = models.ForeignKey(
        to='bot.FieldOfLaw',
        verbose_name='Юридический флаг',
        max_length=255,
        on_delete=models.PROTECT)
    main_question = models.IntegerField(
        verbose_name='Подвопросы',
        default=0,
        )

    def __str__(self):
        return f'#{self.question}'

    class Meta:
        verbose_name = 'Правила'
        verbose_name_plural = 'Правила'


# исковые заявления
class StatementsOfClaim(models.Model):
    title = models.CharField(
        verbose_name='Название',
        max_length=255,
        default='none',
       )
    document = models.FileField(
        verbose_name='Документ',
        upload_to='documents/%Y/%m/%d/',)
    action_algorithm = models.CharField(
        verbose_name='Алгоритм действия',
        max_length=255)
    regulations = models.ManyToManyField(Regulations, verbose_name='Правила',)

    def filename(self):
        return os.path.basename(self.document.name)

    class Meta:
        verbose_name = 'Исковые заявления'
        verbose_name_plural = 'Исковые заявления'
