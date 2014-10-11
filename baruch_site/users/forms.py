from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    # username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(label='Retype password', widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if User.objects.filter(username=username).exists() and username != self.instance.username:
            self._errors['username'] = self.error_class(['Username already in use.'])

        if User.objects.filter(email=email).exists() and email != self.instance.email:
            self._errors['email'] = self.error_class(['This email is already on the system.'])

        if cleaned_data.get('password2') and (cleaned_data.get('password') != cleaned_data.get('password2')):
            error_message = ['Passwords don\'t match']
            self._errors['password'] = self.error_class(error_message)
            self._errors['password2'] = self.error_class(error_message)

        return cleaned_data

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'password2')


class SettingsForm(RegistrationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(), required=False)
    new_password2 = forms.CharField(label='Retype password', widget=forms.PasswordInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm,self).__init__(*args, **kwargs)
        self.fields.pop('password2')

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        not_cleaned_data = self.data

        try:
            user = User.objects.get(username=cleaned_data['username'])
        except User.DoesNotExist:
            error_message = ['You can\'t change your username.']
            self._errors['username'] = self.error_class(error_message)
            return cleaned_data

        if not user.check_password(cleaned_data['password']):
            error_message = ['Wrong password.']
            self._errors['password'] = self.error_class(error_message)

        if not_cleaned_data['new_password1'] != not_cleaned_data['new_password2']:
            error_message = ['Passwords don\'t match.']
            self._errors['new_password1'] = self.error_class(error_message)
            self._errors['new_password2'] = self.error_class(error_message)

        elif (not_cleaned_data['new_password1'] and not_cleaned_data['new_password2']):
            self.cleaned_data['password'] = not_cleaned_data['new_password1']

        
        return cleaned_data


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'new_password1', 'new_password2')