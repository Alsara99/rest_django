from django.contrib.auth.models import AbstractUser
from django.db import models
from materials.models import Course, Lesson


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
        help_text="Укажите электронную почту"
    )
    city = models.CharField(
        verbose_name="Город",
        help_text="Укажите город"
    )
    phone_number = models.CharField(
        max_length=35,
        verbose_name="Номер телефона",
        help_text="Укажите номер телефона"
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватарка",
        help_text="Загрузите аватар"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email


    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["city", "email"]


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(
        verbose_name="Дата",
        help_text="Укажите дату"
    )
    way = models.TextField(
        verbose_name="Способ оплаты",
        help_text="Укажите способ оплаты"
    )
    summ = models.IntegerField(
        verbose_name="Сумма",
        help_text="Укажите сумму"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)


    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["way", "date", "course", "lesson"]