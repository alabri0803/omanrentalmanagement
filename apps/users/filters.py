from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class UserTypeFilter(admin.SimpleListFilter):
    title = _('نوع المستخدم')
    parameter_name = 'user_type'

    def lookups(self, request, model_admin):
        return [
            ('OWNER', _('مالكو العقارات')),
            ('INVESTOR', _('المستثمرون المؤجرون')),
            ('COMPANY', _('الشركات المستأجرة')),
            ('GOVERNMENT', _('الجهات الحكومية')),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user_type=self.value())

class CompanyTypeFilter(admin.SimpleListFilter):
    title = _('نوع الشركة')
    parameter_name = 'company_type'

    def lookups(self, request, model_admin):
        return [
            ('OM', _('شركات عمانية')),
            ('GCC', _('شركات خليجية')),
            ('INT', _('شركات أجنبية')),
        ]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(company_type=self.value())