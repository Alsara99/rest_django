from django.db import models

class Course(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Наименование курса",
        help_text="Укажите наименование курса",
    )
    description = models.TextField(
        verbose_name="Описание курса", help_text="Укажите описание курса"
    )
    preview = models.ImageField(
        upload_to="materials/previews",
        blank=True,
        null=True,
        verbose_name="Превью курса",
        help_text="Укажите превью курса",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["name"]


class Lesson(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название урока",
        help_text="Укажите название урока",
    )
    description = models.TextField(
        verbose_name="Описание урока", help_text="Укажите описание урока"
    )
    preview = models.ImageField(
        upload_to="materials/previews",
        blank=True,
        null=True,
        verbose_name="Превью урока",
        help_text="Укажите превью урока",
    )
    video_link = models.URLField(
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видео"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["name"]
