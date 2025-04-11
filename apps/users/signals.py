from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from .models import User

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.email:
        subject = _('مرحباً بك في نظام إدارة الإيجارات')
        message = render_to_string('users/email/welcome.html', {
            'user': instance,
        })
        send_mail(
            subject,
            message,
            'noreply@rental-system.com',
            [instance.email],
            fail_silently=False,
        )