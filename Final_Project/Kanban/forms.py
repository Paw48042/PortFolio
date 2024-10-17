from django.forms import ModelForm
from .models import User 
from django import forms

class RegisterForm(ModelForm):
    username = forms.CharField(help_text= "", widget= forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs= {'class':'form-control'}))
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs= {'class':'form-control'}))
    profilePic = forms.ImageField(required= False, label= 'Profile Picture',widget=forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['company','username','email', 'password','confirm_password', 'first_name', 'last_name','profilePic']
        widgets = {
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'email' : forms.TextInput(attrs={'class': 'form-control'}),
            'first_name' : forms.TextInput(attrs={'class': 'form-control'}),
            'last_name' : forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("The passwords do not match.")
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(label='Username',widget= forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs= {'class':'form-control'}), label='Password')
