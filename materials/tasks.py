from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_course_update_email(course_id, subscriber_email):
    send_mail(
        'Обновление материала курса',
        f'Материалы курса {course_id} обновлены',
        'daniil.st4r@yandex.ru',
        [subscriber_email]
    )
