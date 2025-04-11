from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'user_type', 'password1', 'password2')
        labels = {
            'user_type': _('نوع المستخدم'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # إعداد RTL للعناصر
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control rtl-input'})

class LoginForm(forms.Form):
    username = forms.CharField(label=_('اسم المستخدم'))
    password = forms.CharField(label=_('كلمة المرور'), widget=forms.PasswordInput)