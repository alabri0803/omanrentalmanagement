from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import User, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = _('الملف الشخصي')
    fields = ('avatar', 'nationality', 'address', 'emergency_contact')
    extra = 0
    
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    inlines = (UserProfileInline,)
    list_display = (
        'email',
        'phone',
        'get_user_type_display',
        'company_name',
        'is_verified',
        'is_active',
    )
    list_filter = (
        'user_type', 
        'company_type',
        'is_verified',
        'is_active',
        'is_staff',
    )
    search_fields = (
        'email',
        'phone',
        'first_name',
        'last_name',
        'company_name',
        'commercial_reg_no'
    )
    fieldsets = (
        (None, {'fields': (
            'email', 
            'password'
        )}),
        (_('المعلومات الشخصية'), {
            'fields': (
                'first_name', 
                'last_name', 
                'id_number',
                'phone',
                'whatsapp',
            )}),
        (_('معلومات الشركة'), {
            'fields': (
                'company_name',
                'company_type',
                'commercial_reg_no',
                'comany_license',
            )}),
        (_('صلاحيات المستخدم'), {
            'fields': (
                'user_type',
                'is_verified',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )}),
        (_('إعدادات خاصة'), {
            'fields': (
                'preferred_language',
                'related_accounts',
                'verification_token'
            ),
            'classes': ('collapse',)
        }),
        (_('تواريخ مهمة'), {
            'fields': (
                'last_login', 
                'date_joined'
            ),
            'classes': ('collapse',)
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 
                'phone', 
                'user_type', 
                'password1', 
                'password2'
            ),
        }),
        (_('معلومات إضافية'), {
            'classes': ('collapse',),
            'fields': (
                'first_name',
                'last_name',
                'company_name',
                'company_type',
            ),
        })
    )
    action = ['verify_users', 'export_users']

    def verify_users(self, request, queryset):
        update = queryset.update(is_verified=True)
        self.message_user(request, f"تم توثيق {update} مستخدم")
    verify_users.short_description = _('توثيق المستخدمين المحددين')

    def export_users(self, request, queryset):
        pass
    export_users.short_description = _('تصدير بيانات المستخدمين')

    def get_company_type(self, obj):
        return obj.get_company_type_display() if obj.company_type else "-"
    get_company_type.short_description = _('نوع الشركة')
    get_company_type.admin_order_field = 'company_type'
    
admin.site.register(User, CustomUserAdmin)