from datetime import date

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

#from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    """مدير مستخدمين متطور مع تحسينات للأمان"""

    def _create_user(self, email, company_name, commercial_registration, password=None, **extra_fields):
        if not email:
            raise ValueError(_('يجب توفير عنوان بريد إلكتروني صحيح'))
        if not company_name:
            raise ValueError(_('يجب توفير اسم الشركة'))
        if not commercial_registration:
            raise ValueError(_('يجب توفير السجل التجاري'))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            company_name=company_name,
            commercial_registration=commercial_registration,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, company_name, commercial_registration, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, company_name, commercial_registration, password, **extra_fields)

    def create_superuser(self, email, company_name, commercial_registration, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('المشرف يجب أن يكون is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('المشرف يجب أن يكون is_superuser=True.'))

        return self._create_user(email, company_name, commercial_registration, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """نموذج مستخدم متطور مع ميزات إضافية"""

    class UserType(models.TextChoices):
        OWNER = 'OWNER', _('مالك المبنى')
        INVESTOR = 'INVESTOR', _('مستثمر المبنى')
        TENANT = 'TENANT', _('مستأجر الوحدة')
        ADMIN = 'ADMIN', _('مدير النظام')

    # معلومات أساسية
    email = models.EmailField(
        _('البريد الإلكتروني'),
        unique=True,
        help_text=_('البريد الإلكتروني الرسمي للشركة')
    )
    company_name = models.CharField(
        _('اسم الشركة'),
        max_length=150,
        help_text=_('الاسم الرسمي للشركة كما في السجل التجاري')
    )
    company_name_english = models.CharField(
        _('اسم الشركة (الإنجليزية)'),
        max_length=150,
        blank=True,
        null=True,
        help_text=_('اسم الشركة باللغة الإنجليزية إن وجد')
    )

    # معلومات قانونية
    commercial_registration = models.CharField(
        _('السجل التجاري'),
        max_length=50,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[0-9]+$',
                message=_('يجب أن يحتوي السجل التجاري على أرقام فقط')
            )
        ],
        help_text=_('رقم السجل التجاري الصادر من الوزارة')
    )
    tax_number = models.CharField(
        _('الرقم الضريبي'),
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        help_text=_('الرقم الضريبي للشركة إن وجد')
    )
    establishment_date = models.DateField(
        _('تاريخ التأسيس'),
        null=True,
        blank=True,
        help_text=_('تاريخ تأسيس الشركة')
    )

    # معلومات الاتصال
    #phone = PhoneNumberField(
        #_('رقم الهاتف الرئيسي'),
        #region='OM',
        #help_text=_('رقم الهاتف الرسمي للشركة')
    #)
    #secondary_phone = PhoneNumberField(
        #_('رقم هاتف احتياطي'),
        #region='OM',
        #blank=True,
        #null=True,
        #help_text=_('رقم هاتف احتياطي للشركة')
    #)
    country = CountryField(
        _('الدولة'),
        default='OM',
        help_text=_('الدولة المسجلة فيها الشركة')
    )
    city = models.CharField(
        _('المدينة'),
        max_length=50,
        default='مسقط',
        help_text=_('المدينة الرئيسية للشركة')
    )
    address = models.TextField(
        _('العنوان التفصيلي'),
        help_text=_('العنوان الرسمي للشركة')
    )
    postal_code = models.CharField(
        _('الرمز البريدي'),
        max_length=20,
        blank=True,
        null=True,
        help_text=_('الرمز البريدي للعنوان')
    )

    # معلومات المستخدم
    user_type = models.CharField(
        _('نوع المستخدم'),
        max_length=10,
        choices=UserType.choices,
        help_text=_('تحديد نوع المستخدم (مالك، مستثمر، مستأجر)')
    )
    company_logo = models.ImageField(
        _('شعار الشركة'),
        upload_to='company_logos/',
        blank=True,
        null=True,
        help_text=_('شعار الشركة الرسمي')
    )
    website = models.URLField(
        _('الموقع الإلكتروني'),
        blank=True,
        null=True,
        help_text=_('الموقع الرسمي للشركة إن وجد')
    )

    # إعدادات الحساب
    is_active = models.BooleanField(
        _('حساب نشط'),
        default=True,
        help_text=_('يحدد ما إذا كان يمكن للمستخدم تسجيل الدخول')
    )
    is_staff = models.BooleanField(
        _('صلاحيات موظف'),
        default=False,
        help_text=_('يحدد ما إذا كان المستخدم يمكنه الوصول إلى لوحة الإدارة')
    )
    is_verified = models.BooleanField(
        _('حساب موثوق'),
        default=False,
        help_text=_('يحدد ما إذا تم التحقق من صحة المستخدم')
    )
    date_joined = models.DateTimeField(
        _('تاريخ التسجيل'),
        auto_now_add=True,
        help_text=_('تاريخ إنشاء الحساب')
    )
    last_updated = models.DateTimeField(
        _('آخر تحديث'),
        auto_now=True,
        help_text=_('تاريخ آخر تعديل على بيانات الحساب')
    )

    # إعدادات المصادقة
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company_name', 'commercial_registration']

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('مستخدم')
        verbose_name_plural = _('المستخدمون')
        ordering = ['company_name']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['company_name']),
            models.Index(fields=['commercial_registration']),
            models.Index(fields=['user_type']),
        ]

    def __str__(self):
        return f"{self.company_name} ({self.get_user_type_display()})"

    @property
    def company_age(self):
        """حساب عمر الشركة بالسنوات"""
        if self.establishment_date:
            today = date.today()
            return today.year - self.establishment_date.year - (
                (today.month, today.day) < (self.establishment_date.month, self.establishment_date.day)
            )
        return None

class Owner(models.Model):
    """نموذج متطور لمالك المبنى"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        limit_choices_to={'user_type': User.UserType.OWNER},
        verbose_name=_('حساب المستخدم'),
        related_name='owner_profile'
    )
    ownership_percentage = models.DecimalField(
        _('نسبة الملكية'),
        max_digits=5,
        decimal_places=2,
        default=100.00,
        help_text=_('نسبة ملكية المالك في المبنى')
    )
    bank_name = models.CharField(
        _('اسم البنك'),
        max_length=100,
        blank=True,
        null=True,
        help_text=_('البنك الذي يتلقى المالك مدفوعاته منه')
    )
    iban_number = models.CharField(
        _('رقم الآيبان'),
        max_length=30,
        blank=True,
        null=True,
        validators=[RegexValidator(
            regex='^[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}$',
            message=_('يجب إدخال رقم آيبان صحيح')
        )],
        help_text=_('رقم الآيبان لتحويل الأرباح')
    )
    preferred_payment_method = models.CharField(
        _('طريقة الدفع المفضلة'),
        max_length=20,
        choices=[
            ('BANK', _('تحويل بنكي')),
            ('CHEQUE', _('شيك')),
            ('CASH', _('نقدي')),
        ],
        default='BANK',
        help_text=_('الطريقة المفضلة لاستلام المدفوعات')
    )

    class Meta:
        verbose_name = _('مالك')
        verbose_name_plural = _('الملاك')

    def __str__(self):
        return f"{self.user.company_name} ({self.ownership_percentage}%)"

class Investor(models.Model):
    """نموذج متطور لمستثمر المبنى"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        limit_choices_to={'user_type': User.UserType.INVESTOR},
        verbose_name=_('حساب المستخدم'),
        related_name='investor_profile'
    )
    investment_amount = models.DecimalField(
        _('مبلغ الاستثمار'),
        max_digits=12,
        decimal_places=2,
        default=0.00,
        help_text=_('المبلغ الذي استثمره المستثمر')
    )
    investment_percentage = models.DecimalField(
        _('نسبة الاستثمار'),
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text=_('نسبة الاستثمار في الأرباح')
    )
    investment_date = models.DateField(
        _('تاريخ الاستثمار'),
        help_text=_('تاريخ بداية الاستثمار')
    )
    contract_duration = models.PositiveIntegerField(
        _('مدة العقد (سنوات)'),
        default=1,
        help_text=_('مدة عقد الاستثمار بالسنوات')
    )
    bank_details = models.JSONField(
        _('تفاصيل البنك'),
        blank=True,
        null=True,
        help_text=_('تفاصيل الحساب البنكي لتحويل الأرباح')
    )

    class Meta:
        verbose_name = _('مستثمر')
        verbose_name_plural = _('المستثمرون')

    def __str__(self):
        return f"{self.user.company_name} ({self.investment_percentage}%)"

    @property
    def contract_end_date(self):
        """حساب تاريخ انتهاء عقد الاستثمار"""
        if self.investment_date:
            return self.investment_date.replace(
                year=self.investment_date.year + self.contract_duration
            )
        return None

class Tenant(models.Model):
    """نموذج متطور للمستأجر (شركة)"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        limit_choices_to={'user_type': User.UserType.TENANT},
        verbose_name=_('حساب المستخدم'),
        related_name='tenant_profile'
    )
    company_activity = models.CharField(
        _('نشاط الشركة'),
        max_length=100,
        help_text=_('النشاط التجاري الرئيسي للشركة المستأجرة')
    )
    authorized_person = models.CharField(
        _('الشخص المفوض'),
        max_length=100,
        help_text=_('اسم الشخص المفوض بالتوقيع عن الشركة')
    )
    authorized_person_id = models.CharField(
        _('رقم هوية المفوض'),
        max_length=20,
        help_text=_('رقم هوية الشخص المفوض')
    )
    emergency_contact = models.CharField(
        _('جهة اتصال الطوارئ'),
        max_length=100,
        blank=True,
        null=True,
        help_text=_('اسم جهة الاتصال في حالات الطوارئ')
    )
    #emergency_phone = PhoneNumberField(
        #_('هاتف الطوارئ'),
        #region='OM',
        #blank=True,
        #null=True,
        #help_text=_('رقم هاتف الطوارئ')
    #)
    insurance_policy = models.CharField(
        _('بوليصة التأمين'),
        max_length=50,
        blank=True,
        null=True,
        help_text=_('رقم بوليصة التأمين على المحتويات إن وجدت')
    )
    insurance_expiry = models.DateField(
        _('انتهاء التأمين'),
        blank=True,
        null=True,
        help_text=_('تاريخ انتهاء بوليصة التأمين')
    )

    class Meta:
        verbose_name = _('مستأجر')
        verbose_name_plural = _('المستأجرون')

    def __str__(self):
        return f"{self.user.company_name} ({self.company_activity})"

    @property
    def has_valid_insurance(self):
        """تحقق مما إذا كان التأمين ساري المفعول"""
        if self.insurance_expiry:
            return self.insurance_expiry >= date.today()
        return False