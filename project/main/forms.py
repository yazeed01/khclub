
from django import forms
from .models import Contact_Me



class Contact_Me_Form(forms.ModelForm):
    
    class Meta:
        model = Contact_Me
        fields = ["first_name","email" ,"message"]