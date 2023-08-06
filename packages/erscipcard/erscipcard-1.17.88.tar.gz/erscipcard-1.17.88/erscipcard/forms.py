from django import forms
from .models import User1
from .widget import AvatarFileUploadInput
from .widget import JalaliDateWidget

class User1form(forms.ModelForm):
    class Meta:
        model = User1
        fields = "__all__"
        widgets = { "etebar": JalaliDateWidget , "pic": AvatarFileUploadInput  }


