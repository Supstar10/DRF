# Generated by Django 5.1.3 on 2024-11-21 11:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0002_alter_course_lessons"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="course",
            name="lessons",
        ),
        migrations.AddField(
            model_name="lesson",
            name="course",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="materials.course",
                verbose_name="курсы",
            ),
        ),
    ]