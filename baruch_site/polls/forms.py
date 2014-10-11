from django import forms
from models import Cork
from models import Basket

class CorkForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    image_url = forms.URLField(label='Image URL', required=False)
 
    def clean(self):
        cleaned_data = self.cleaned_data

        image = cleaned_data.get('image', None)
        image_url = cleaned_data.get('image_url', None)

        if image and image_url: # both were entered
            raise forms.ValidationError("Enter only one of image file or image url")
        # elif not image and not image_url: # neither were entered
        #     raise forms.ValidationError("You must upload an image or paste a link for your cork")


        return cleaned_data

    class Meta:
        model = Cork
        fields = ('owner', 'question', 'image', 'image_url', 'pub_date', 'update', 'references', 'tags', 'private')
        exclude = ['owner', 'pub_date', 'update', 'references']
        widgets = {
          'question': forms.Textarea(attrs={'rows':2, 'cols':40}),
        }


class BasketForm(forms.ModelForm):

    class Meta:
        model = Basket
        exclude = ['owner', 'pub_date', 'update']
        widgets = {
          'name': forms.Textarea(attrs={'rows':2, 'cols':40}),
        }
