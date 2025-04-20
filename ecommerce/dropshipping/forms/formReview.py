# forms.py
from django import forms
from dropshipping.models.reviewsModel import Review

class ReviewForm(forms.ModelForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico',
            'required': 'required'
        }),
        label='Email'
        )
    class Meta:
        model = Review
        fields = ['email', 'rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'class': 'form-control', 'required': 'required'}),
            'comment': forms.Textarea(attrs={'rows': 2 , 'class': 'form-control', 'placeholder': 'Comentario'}),
        }

        
