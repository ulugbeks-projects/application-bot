from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application
import gspread
from google.oauth2.service_account import Credentials
from environs import Env
import json

env = Env()
env.read_env()


service_account = env.str('service_account')
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
    return client.open_by_key('1MkTFL0KwswFPKUtJ5oTQRjbN5dwJMdwHCGymmNUJoMQ').worksheet('Applications')


@receiver(post_save, sender=Application)
def add_application_to_google_sheet(sender, instance, created, **kwargs):
    if created:  # faqat yangi yaratilganda ishlaydi
        worksheet = get_google_sheet()
        worksheet.append_row([
            instance.id,
            instance.full_name,
            instance.phone,
            instance.about,
            instance.resume_file_link or '',
            instance.user.username or '',
            instance.status,
            instance.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        ])
