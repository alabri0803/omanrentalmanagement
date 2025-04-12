from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from .models import User


@receiver(post_save, sender=User)
def handle_user_creation(sender, instance, created, **kwargs):
    if created:
        if instance.email:
            send_verification_email(instance)

    if hasattr(instance, 'profile'):
        return Profile.objects.create(user=instance)

def send_verification_email(user):
    subject = _('تفعيل حسابك في نظام إدارة الإيجارات')
    message = render_to_string('emails/verify_account.html', {'user': user, 'verification_token': user.verification_token})
    send_mail(subject, message, 'no-reply@rental-management.com', [user.email], fail_silently=False)