from django import forms
from django.core.exceptions import ValidationError
from .models import Question

class questionform (forms.Form):
    q_text= forms.CharField()

    def clean(self):
        cleaned_data= super(questionform, self).clean()
        q_text= cleaned_data.get("q_text")
        qq= Question.objects.filter(question_text=q_text)
        if qq:
            raise forms.ValidationError("That quest is already asken")

        return cleaned_data
