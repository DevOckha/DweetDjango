from django import forms 
from .models import Dweet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class DweetForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                'placeholder': 'Dweet something...',
                'class': 'textarea is-success is-medium',
            }

        ),
        label="",
    )

    class Meta:
        model = Dweet
        exclude = ('user', )



class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Enter Username', max_length=128, min_length=4)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # def clean_username(self):
    #     username = self.cleaned_data['username'].lower()
    #     username_exists = User.objects.filter(username=username)

    #     if username_exists:
    #         raise forms.ValidationError("Username already exists")
    #     return username


    # def clean_email(self):
    #     email = self.cleaned_data['email'].lower()
    #     email_exist = User.objects.filter(email=email)

    #     if email_exist:
    #         raise forms.ValidationError("Email already exists")
    #     return email
    
    # def clean_password2(self):
    #     password1 = self.cleaned_data['password1']
    #     password2 = self.cleaned_data['password2']

    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Passowrd don't match")
        
    #     return password2
    
    # def save(self, commit=True):
    #     user = User.objects.create(
    #         self.cleaned_data['username'],
    #         self.cleaned_data['email'],
    #         self.cleaned_data['password1']
    #     )

    #     return user

