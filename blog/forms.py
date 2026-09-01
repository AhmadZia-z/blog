from django import forms
from django.core.validators import ValidationError
from .models import Message


class ContactUsForm(forms.Form):
    birth_year_choices = ['1980', '1981', '1982']
    name = forms.CharField(max_length=30, label='your name')
    text = forms.CharField(max_length=10, label='your message')
    birth_year = forms.DateField(widget=forms.SelectDateWidget(years=birth_year_choices, attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        name = self.cleaned_data.get('name')
        text = self.cleaned_data.get('text')
        if name == text:
            raise ValidationError('name and text are same', code='name_text_same')
        return cleaned_data


    def clean_name(self):
        name = self.cleaned_data.get('name')
        if ' ' in name:
            raise ValidationError('can not use space in name', code='a in name')
        return name



class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'enter your title'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'enter your message'
            })
        }