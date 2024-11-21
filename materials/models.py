from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Название курса",
        help_text="Укажите название курса",
    )
    preview = models.ImageField(
        upload_to="materials/course",
        **NULLABLE,
        verbose_name="Превью",
        help_text="Добавьте фото",
    )
    description = models.TextField(
        **NULLABLE, verbose_name="Описание", help_text="Добавьте описание"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=50, verbose_name="Название урока", help_text="Укажите название урока"
    )
    preview = models.ImageField(
        upload_to="materials/lesson",
        **NULLABLE,
        verbose_name="Превью",
        help_text="Добавьте фото",
    )
    description = models.TextField(
        verbose_name="Описание",
        **NULLABLE,
        help_text="Добавьте описание",
    )
    link = models.URLField(
        max_length=200,
        **NULLABLE,
        verbose_name="ссылка на видео",
        help_text="Укажите ссылку на видео",
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="курсы", **NULLABLE
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
