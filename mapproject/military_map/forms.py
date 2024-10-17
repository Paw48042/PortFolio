from django.forms import ModelForm
from .models import CustomUser, Mission
from django import forms 
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class RegisterForm(ModelForm):
    email = forms.EmailField(label= "E-mail", widget = forms.EmailInput(attrs= {'class': 'form-control'}))
    username = forms.CharField(help_text= "", widget= forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs= {'class':'form-control'}))
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs= {'class':'form-control'}))
    first_name = forms.CharField(label = 'ยศ-ชื่อ', widget = forms.TextInput(attrs= {'class': 'form-control'}))
    last_name = forms.CharField(label = 'นามสกุล',widget= forms.TextInput(attrs = {'class' : 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name' ,'email', 'password']
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("ไอดีนี้ถูกใช้แล้ว ไม่สามารถใช้ซ้ำได้")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email = email).exists():
            raise ValidationError("อีเมลนี้ถูกใช้แล้ว ไม่สามารถใช้ซ้ำได้")
        return email

    

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password:
            if password != confirm_password:
                self.add_error('confirm_password', 'Passwords do not match.')
        
        return cleaned_data
    

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(help_text= "", widget= forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs= {'class':'form-control'}))

class CreateMissionForm(ModelForm):

    name = forms.CharField(help_text= "", widget= forms.TextInput(attrs={'class': 'form-control',
                                                                         'placeholder' : 'ภารกิจแบบใด'}))
    detail = forms.CharField( 
        widget = forms.Textarea(attrs={
            'placeholder': 'รายละเอียดภารกิจ',
            'rows': 4,
            'cols': 40,
            'class' : 'form-control',
        })
        )
    
    class Meta:
        model = Mission
        fields = ['name', 'detail']
        