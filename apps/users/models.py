from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class UserTypes(models.TextChoices):
        OWNER = 'OWNER', _('مالك العقار')
        INVESTOR = 'INVESTOR', _('مستثمر مؤجرة')
        COMPANY = 'COMPANY', _('شركة مستأجرة')
        
    class CompanyNationality(models.TextChoices):
        OMANI = 'OMANI', _('عماني')
        GULF = 'GULF', _('خليجي')
        FOREIGN = 'INT', _('أجنبي')

    user_type = models.CharField(
        max_length=10,  
        choices=UserTypes.choices,
        verbose_name=_('نوع المستخدم')
    )
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("رقم الهاتف يجب أن يكون بتنسيق:'+96812345678'"),
    )
    phone = models.CharField(
        validators=[phone_regex], 
        max_length=17, 
        unique=True,
        verbose_name=_('رقم الهاتف')
    )
    
    company_name = models.CharField(
        max_length=100,  
        blank=True,  
        null=True,
        verbose_name=_('اسم الشركة')
    )
    company_nationality = models.CharField(
        max_length=5,
        choices=CompanyNationality.choices,
        blank=True,
        null=True,
        verbose_name=_('جنسية الشركة')
    )
    commercial_registration = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_('السجل التجاري')
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name=_('حساب موثوق')
    )
    language = models.CharField(
        max_length=5,
        choices=[('ar', 'العربية'), ('en', 'English')],
        default='ar',
        verbose_name=_('اللغة المفضلة')
    )

    class Meta:
        verbose_name = _('مستخدم')
        verbose_name_plural = _('المستخدمون')
        ordering = ['-date_joined']

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