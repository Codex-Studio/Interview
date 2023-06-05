from django.db import models

from apps.users.models import TelegramUser

# Create your models here.
class Question(models.Model):
    user = models.ForeignKey(
        TelegramUser, on_delete=models.SET_NULL,
        verbose_name="Пользователь", 
        blank=True, null=True
    )
    title = models.CharField(
        max_length=500,
        verbose_name="Вопрос"
    )
    point = models.DecimalField(
        verbose_name="Оценка",
        max_digits=2,
        decimal_places=1,
        blank=True, null=True
    )

    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

class Task(models.Model):
    user = models.ForeignKey(
        TelegramUser, on_delete=models.SET_NULL,
        verbose_name="Пользователь", 
        blank=True, null=True
    )
    title = models.CharField(
        max_length=500,
        verbose_name="Задача"
    )
    point = models.DecimalField(
        verbose_name="Оценка",
        max_digits=2,
        decimal_places=1,
        blank=True, null=True
    )

    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

class Mailing(models.Model):
    user = models.ForeignKey(
        TelegramUser, on_delete=models.SET_NULL,
        related_name="user_mailing",
        verbose_name="Пользователь",
        blank=True, null=True
    )
    title = models.CharField(
        max_length=500,
        verbose_name="Сообщение",
    )
    CHOICE_TYPE = (
        ('Start', 'Start'),
        ('Simple', 'Simple'),
        ('End', 'End'),
        ('Personal', 'Personal')
    )
    mailing_type = models.CharField(
        max_length=100,
        choices=CHOICE_TYPE,
        verbose_name="Тип рассылки"
    )

    def __str__(self):
        return self.title 
    
    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"