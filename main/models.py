from django.db import models
from botapp.models import BotUser


class Application(models.Model):
    """
    Application modeli | arizalar uchun model

    Botga ariza yuborish uchun foydalanuvchilar uchun model

    """
    # Ariza yuboruvchi foydalanuvchi
    user = models.ForeignKey(BotUser, on_delete=models.CASCADE, related_name='applications')

    # Ariza yuboruvchi foydalanuvchi ism familiyasi
    full_name = models.CharField(max_length=255)

    # Ariza yuboruvchi telefon raqami
    phone = models.CharField(max_length=15)

    # Ariza yuboruvchi haqida batafsil ma'lumot
    about = models.TextField()

    # Ariza yuboruvchi rezyume fayli
    resume_file_id = models.CharField(max_length=255)
    resume_file_link = models.URLField(null=True, blank=True)

    # Ariza yuborilgan vaqti
    created_at = models.DateTimeField(auto_now_add=True)

    # Ariza oxirgi marta yangilangan vaqti
    updated_at = models.DateTimeField(auto_now=True)

    # Ariza holati

    status_choices = (
        ('new', 'Yangi'),
        ('in_progress', 'Jarayonda'),
        ('accepted', 'Tasdiqlandi'),
        ('rejected', 'Rad etildi'),
    )
    status = models.CharField(max_length=20, choices=status_choices, default='new')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        ordering = ['-created_at']