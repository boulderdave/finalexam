from django import forms
from .models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('answer',)

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.initial['answer'] = ''

    def clean_answer(self):
        if self.instance.answer != self.cleaned_data['answer']:
            self.add_error('answer', "This answer is not correct.")
        else:
            return self.cleaned_data['answer']
