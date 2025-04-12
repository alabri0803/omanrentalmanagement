from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
          'email', 
          'phone', 
          'user_type', 
        )
        labels = {
            'user_type': _('نوع المستخدم'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = False
        self.fields['password2'].required = False

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'