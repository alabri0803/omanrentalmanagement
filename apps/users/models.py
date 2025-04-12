from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
  def create_user(self, email, company_name, password=None, **extra_fields):
    if not email:
      raise ValueError('يجب توفير عنوان البريد الإلكتروني')
    if not company_name:
      raise ValueError('يجب توفير اسم الشركة')
    email = self.normalize_email(email)
    user = self.model(email=email, company_name=company_name, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, email, company_name, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    return self.create_user(email, company_name, password, **extra_fields)

class User(AbstractUser, PermissionsMixin):
  class UserType(models.TextChoices):
    OWNER = 'OWNER', _('مالك المبني')
    INVESTOR = 'INVESTOR', _('مستثمر المبني')
    TENANT = 'TENANT', _('مستأجر الوحدة')
  # الحقول الأساسية
  email = models.EmailField(_('البريد الإلكتروني'), unique=True)
  company_name = models.CharField(_('اسم الشركة'), max_length=100)
  commercial_registration = models.CharField(_('السجل التجاري'), max_length=50, unique=True)
  phone = models.CharField(_('رقم الهاتف'), max_length=20)
  address = models.TextField(_('عنوان الشركة'))
  # نوع المستخدم
  user_type = models.CharField(_('نوع المستخدم'), max_length=10, choices=UserType.choices)
  # الحقول الإدارية
  is_active = models.BooleanField(_('نشط'), default=True)
  is_staff = models.BooleanField(_('موظف'), default=False)
  date_joined = models.DateTimeField(_('تاريخ التسجيل'), auto_now_add=True)
  # إعدادات المصادقة
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['company_name', 'commercial_registration']
  objects = UserManager()

  class Meta:
    verbose_name = _('المستخدم')
    verbose_name_plural = _('المستخدمون')

  def __str__(self):
    return f"{self.company_name} ({self.get_user_type_display()})"

class Owner(models.Model):
  """نموذج مالك المبني (شركة)"""
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, limit_choices_to={'user_type': User.UserType.OWNER}, verbose_name=_('حساب المستخدم'))
  #owned_buildings = models.ManyToManyField('buildings.Building', verbose_name=_('المباني المملوكة'), blank=True)

  class Meta:
    verbose_name = _('مالك')
    verbose_name_plural = _('الملاك')

  def __str__(self):
    return self.user.company_name

class Investor(models.Model):
  """نموذج مستثمر المبني (شركة)"""
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, limit_choices_to={'user_type': User.UserType.INVESTOR}, verbose_name=_('حساب المستخدم'))
  investment_percentage = models.DecimalField(_('نسبة الاستثمار'), max_digits=5, decimal_places=2, default=0.00)

  class Meta:
    verbose_name = _('مستثمر')
    verbose_name_plural = _('المستثمرون')

  def __str__(self):
    return f"{self.user.company_name} ({self.investment_percentage}%)"

class Tenant(models.Model):
  """نموذج مستأجر (شركة)"""
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, limit_choices_to={'user_type': User.UserType.TENANT}, verbose_name=_('حساب المستخدم'))
  #leased_units = models.ManyToManyField('units.Unit', verbose_name=_('الوحدات المؤجرة'), blank=True)

  class Meta:
    verbose_name = _('مستأجر')
    verbose_name_plural = _('المستأجرون')

  def __str__(self):
    return self.user.company_name