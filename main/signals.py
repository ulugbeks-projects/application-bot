from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application
import gspread
from google.oauth2.service_account import Credentials


def get_google_sheet():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", 
              "https://www.googleapis.com/auth/drive.file", 
              "https://www.googleapis.com/auth/drive"]

    credentials = Credentials.from_service_account_file(
        'service_account.json',
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
