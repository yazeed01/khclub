from django.forms import ModelForm
from .models import CorrectAnswer

class CorrectAnswerForm(ModelForm):
    
    class Meta:
            model = CorrectAnswer
            exclude = ['correct_answer','created_by']