from django.db import models
import random, string

# Create your models here.
class TelegramUser(models.Model):
    user_id = models.CharField(
        max_length=300,
        verbose_name="ID пользователя",
        blank=True, null=True
    )
    chat_id = models.CharField(
        max_length=300,
        verbose_name="Chat ID",
        blank=True, null=True
    )
    username = models.CharField(
        max_length=300,
        verbose_name="Имя пользователя",
        blank=True, null=True
    )
    last_name = models.CharField(
        max_length=300,
        verbose_name="Имя",
        blank=True, null=True
    )
    first_name = models.CharField(
        max_length=300,
        verbose_name="Фамилия",
        blank=True, null=True
    )
    code = models.CharField(
        max_length=10, unique=True,
        blank=True, null=True
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата регистрации"
    )

    def __str__(self):
        return f"{self.id} {self.username}"
    
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        return super().save(*args, **kwargs)

    @staticmethod
    def generate_code():
        characters = string.ascii_letters + string.digits
        code = ''.join(random.choice(characters) for _ in range(6)).upper()
        return code
    
    class Meta:
        verbose_name = "Телеграм пользователь"
        verbose_name_plural = "Телеграм пользователи"