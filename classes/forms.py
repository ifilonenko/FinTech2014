from django import forms
from models import Class

class ClassForm(forms.ModelForm):

    class Meta:
        model = Class
        exclude = ['owner', 'pub_date', 'update', 'enrollment', 'baskets']
        widgets = {
          'name': forms.Textarea(attrs={'rows':2, 'cols':40}),
        }