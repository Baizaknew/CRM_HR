from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model

from django.core.mail import EmailMultiAlternatives

import requests
from django.template.loader import render_to_string
from django.utils.html import strip_tags


User = get_user_model()

@shared_task
def send_email_notification(subject: str, users_emails: [str], context: dict, template_name: str):
    html_template = render_to_string(template_name, context)
    text_template = strip_tags(html_template)
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_template,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[users_emails],
    )

    email.attach_alternative(html_template, "text/html")
    email.send()
    return True


@shared_task
def send_telegram_notification(text: str):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": settings.TELEGRAM_HR_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
    }
    requests.post(url, data=data)
    return True
