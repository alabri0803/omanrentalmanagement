from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    USER_TYPES = (
        ('OWNER', _('مالك العقار')),
        ('INVESTOR', _('مستثمر')),
        ('TENANT', _('مستأجر')),
        ('COMPANY', _('شركة')),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    phone = models.CharField(max_length=20, unique=True)
    is_verified = models.BooleanField(default=False)
    language = models.CharField(max_length=5, choices=[('ar', 'العربية'), ('en', 'English')], default='ar')

    class Meta:
        verbose_name = _('مستخدم')
        verbose_name_plural = _('المستخدمون')

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"