from django import forms
from .models import User1
from .widget import AvatarFileUploadInput
from .widget import JalaliDateWidget

class User1form(forms.ModelForm):
    class Meta:
        model = User1
        #fields = "__all__"
        exclude = ['address','reserv1','reserv2','reserv3','reserv4',]
        widgets = { "etebar": JalaliDateWidget , "pic": AvatarFileUploadInput  }


