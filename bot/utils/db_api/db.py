from asgiref.sync import sync_to_async
from botapp.models import BotUser
from main.models import Application
import logging


@sync_to_async
def get_or_create_user(user_id, username, first_name, last_name, language_code: str|None = None):
    user, created = BotUser.objects.get_or_create(
        user_id=user_id,
        defaults={
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'language_code': language_code
        }
    )
    return user, created


@sync_to_async
def create_application(user_id, full_name, phone_number, about_myself, resume_file_id, resume_file_link):
    try:
        user = BotUser.objects.get(user_id=user_id)

        application = Application.objects.create(
            user=user,
            full_name=full_name,
            phone=phone_number,
            about=about_myself,
            resume_file_id=resume_file_id,
            resume_file_link=resume_file_link
        )
        return application
    
    except Exception as err:
        logging.error(err)
        return None