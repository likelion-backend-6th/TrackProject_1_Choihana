from django import forms
from .models import ReviewRating


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['review','rating']
        widgets ={
            'review' : forms.Textarea(attrs={'rows':3, 'cols':50})
        }
