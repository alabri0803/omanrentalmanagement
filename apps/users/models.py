import uuid

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name=_('البريد الإلكتروني')
    )
    class UserTypes(models.TextChoices):
        OWNER = 'OWNER', _('مالك العقار')
        INVESTOR = 'INVESTOR', _('مستثمر مؤجرة')
        COMPANY = 'COMPANY', _('شركة مستأجرة')
        GOVERNMENT = 'GOVERNMENT', _('جهة حكومية')
        
    class CompanyNationality(models.TextChoices):
        OMANI = 'OM', _('عماني')
        GULF = 'GCC', _('خليجي')
        FOREIGN = 'INT', _('أجنبي')
        MIXED = 'MIX', _('مختلط عماني واجنبي')

    user_type = models.CharField(
        max_length=10,  
        choices=UserTypes.choices,
        verbose_name=_('نوع المستخدم'),
        default=UserTypes.COMPANY
    )
    id_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_('رقم الهوية')
    )
    phone_regex = RegexValidator(
        regex=r'^\+?968\d{8}$',
        message=_("يجب أن يبدأ رقم الهاتف بــ +968 ويتبعه 8 أرقام")
    )
    phone = models.CharField(
        validators=[phone_regex], 
        max_length=12, 
        unique=True,
        verbose_name=_('هاتف عماني')
    )
    whatsapp = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_('واتساب')
    )
    company_name = models.CharField(
        max_length=100,  
        blank=True,  
        null=True,
        verbose_name=_('اسم الشركة')
    )
    company_type = models.CharField(
        max_length=5,
        choices=CompanyNationality.choices,
        blank=True,
        null=True,
        verbose_name=_('نوع الشركة')
    )
    commercial_reg_no = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_('رقم السجل التجاري')
    )
    comany_license = models.FileField(
        upload_to='company_licenses/',
validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'png'])],
        blank=True,
        null=True,
        verbose_name=_('رخصة الشركة')
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_('حساب موثوق')
    )
    verification_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        verbose_name=_('رمز التحقق')
    )
    preferred_language = models.CharField(
        max_length=5,
        choices=[('ar', 'العربية'), ('en', 'English')],
        default='ar',
        verbose_name=_('اللغة المفضلة')
    )
    related_accounts = models.ManyToManyField(
        'self',
        blank=True,
        verbose_name=_('الحسابات المرتبطة')
    )
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'user_type']

    class Meta:
        verbose_name = _('مستخدم')
        verbose_name_plural = _('المستخدمون')
        ordering = ['-date_joined']
        permissions = [
            ('can_manage_properties', _('يمكنه إدارة العقارات')),
            ('can_view_reports', _('يمكنه عرض التقارير')),
        ]

    def __str__(self):
        if self.user_type == self.UserTypes.COMPANY:
            return f"{self.company_name} ({self.get_company_nationality_display()})"
        return f"{self.username} ({self.get_user_type_display()})"

    def save(self, *args, **kwargs):
        if self.user_type != self.UserTypes.COMPANY:
            self.company_name = None
            self.company_nationality = None
            self.commercial_registration = None
        super().save(*args, **kwargs)

    @property
    def is_owner(self):
        return self.user_type == self.UserTypes.OWNER

    @property
    def is_investor(self):
        return self.user_type == self.UserTypes.INVESTOR

    @property
    def is_company(self):
        return self.user_type == self.UserTypes.COMPANY

    @property
    def is_government(self):
        return self.user_type == self.UserTypes.GOVERNMENT

    def get_contact_info(self):
        return {
            'phone': self.phone,
            'whatsapp': self.whatsapp,
            'email': self.email
        }

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('المستخدم')
    )
    avatar = models.ImageField(
        upload_to='user_avatars/',
        blank=True,
        null=True,
        verbose_name=_('الصورة الشخصية')
    )
    nationality = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('الجنسية')
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_('العنوان')
    )
    emergency_contact = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name=_('جهة اتصال طوارئ')
    )

    class Meta:
        verbose_name = _('ملف تعريفي')
        verbose_name_plural = _('الملفات تعريفية')

    def __str__(self):
        return f"ملف {self.user.email}"