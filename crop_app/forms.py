from django import forms
from .models import LeafImage, Comment, Reaction, Contact

class ImageUploadForm(forms.Form):
    image = forms.ImageField()


class LeafImageForm(forms.ModelForm):
    class Meta:
        model = LeafImage
        fields = ['image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'text']


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'you@example.com'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your message...',
                'style': 'height: 100px;'
            }),
        }
