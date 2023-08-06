from django import forms
from .models import User1
from .widget import AvatarFileUploadInput
from .widget import JalaliDateWidget
from django.conf import settings

class User1form(forms.ModelForm):
    class Meta:
        model = User1
        #fields = "__all__"
        exclude = settings.ERSCIPCARD_VARS['exclude'] if hasattr(settings, 'ERSCIPCARD_VARS') and settings.ERSCIPCARD_VARS['exclude'] else ['address','reserv1','reserv2','reserv3','reserv4',]
        labels = settings.ERSCIPCARD_VARS['labels'] if hasattr(settings, 'ERSCIPCARD_VARS') and settings.ERSCIPCARD_VARS['labels'] else {}
        widgets = { "etebar": JalaliDateWidget , "pic": AvatarFileUploadInput  }


