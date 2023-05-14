from django import forms

from .models import Review


class Review_form(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['review_text']

