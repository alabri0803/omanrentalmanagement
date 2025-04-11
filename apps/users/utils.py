import random
import string
from django.utils.translation import gettext_lazy as _

def generate_temp_password(length=8):
    """إنشاء كلمة مرور مؤقتة"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def send_password_reset(user):
    """إرسال كلمة مرور مؤقتة"""
    temp_pass = generate_temp_password()
    user.set_password(temp_pass)
    user.save()

    # إرسال البريد الإلكتروني
    message = _("""
    كلمة المرور المؤقتة الخاصة بك: {password}
    يرجى تغييرها بعد تسجيل الدخول.
    """).format(password=temp_pass)

    send_mail(
        _('إعادة تعيين كلمة المرور'),
        message,
        'noreply@rental-system.com',
        [user.email],
        fail_silently=False,
    )