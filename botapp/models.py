from django.db import models


# BotUser modeli | foydalanuvchilar uchun model
class BotUser(models.Model):
    """
    BotUser modeli | foydalanuvchilar uchun model

    Botga start bosgan foydalanuvchilarni saqlash uchun model

    """
    # Telegram user id | user id har bir telegram tomonidan beriladi va har biri unikal bo'ladi
    user_id = models.CharField(max_length=255, unique=True) 

    # Telegram user first name | foydaluvchi ismi (telegramdan olinadi)
    first_name = models.CharField(max_length=255)

    # Telegram user last name | foydaluvchi familiyasi (telegramdan olinadi agar mavjud bo'lsa)
    last_name = models.CharField(max_length=255, blank=True, null=True) # *ixtiyoriy

    # Telegram user username | foydaluvchi nomi (telegramdan olinadi agar mavjud bo'lsa)
    username = models.CharField(max_length=255, blank=True, null=True) # *ixtiyoriy

    # Telegram user language code | foydaluvchi til kodi (telegramdan olinadi)
    language_code = models.CharField(max_length=4, default='uz')

    # Telegram user is active | foydaluvchi faolmi yoki yo'qmi
    is_active = models.BooleanField(default=True) # foydalanuvchini harakatlarini cheklash uchun

    # Telegram user is admin | foydaluvchi adminmi yoki yo'qmi
    is_admin = models.BooleanField(default=False)

    # Telegram user joined date and time | foydaluvchi qo'shilgan vaqti
    created_at = models.DateTimeField(auto_now_add=True)

    # Telegram user last update date and time | foydaluvchi oxirgi marta yangilangan vaqti
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name


    class Meta:
        verbose_name = 'Bot User'
        verbose_name_plural = 'Bot Users'
        ordering = ['-created_at']
