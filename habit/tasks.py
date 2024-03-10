import os

import requests

from celery import shared_task
from django.contrib.auth import get_user_model
from habit.services import get_habits_due_now


@shared_task
def send_reminder():
    """
    Sending a reminder to perform an action
    """
    URL = os.getenv('TELEGRAM_URL')
    TOKEN = os.getenv('TELEGRAM_API_TOKEN')

    # Get habits due now
    for user in get_user_model().objects.all():
        habits_due_now = get_habits_due_now(user)

        for habit in habits_due_now:
            chat_id = user.telegram
            message = f"It's time to do {habit.action}."
            try:
                requests.post(
                    url=f'{URL}{TOKEN}/sendMessage?chat_id={chat_id}&text={message}'
                )
            except requests.exceptions.RequestException as e:
                # Log the error or handle it as needed
                print(f"Failed to send message to {chat_id}: {e}")
