from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import BotUser
import gspread
from google.oauth2.service_account import Credentials
from environs import Env
import json

env = Env()
env.read_env()


service_account = env.str('GOOGLE_SERVICE_ACCOUNT')
if service_account:
    with open('service_account.json', 'w') as f:
        json.dump(json.loads(service_account), f, indent=4)

    print("✅ service_account.json yaratildi.")
else:
    raise Exception("❌ GOOGLE_SERVICE_ACCOUNT_JSON topilmadi.")

def get_google_sheet():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", 
              "https://www.googleapis.com/auth/drive.file", 
              "https://www.googleapis.com/auth/drive"]

    credentials = Credentials.from_service_account_file(
        service_account,
        scopes=scopes
    )

    client = gspread.authorize(credentials)
    return client.open_by_key('1MkTFL0KwswFPKUtJ5oTQRjbN5dwJMdwHCGymmNUJoMQ').worksheet('Bot Users')


@receiver(post_save, sender=BotUser)
def add_bot_user_to_google_sheet(sender, instance, created, **kwargs):
    if created:  # faqat yangi yaratilganda ishlaydi
        worksheet = get_google_sheet()
        worksheet.append_row([
            instance.id,
            instance.user_id,
            instance.first_name,
            instance.last_name or '',
            instance.username or '',
            'Active' if instance.is_active else 'Inactive',
            'Admin' if instance.is_admin else 'User',
            instance.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        ])
