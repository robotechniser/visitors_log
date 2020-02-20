from django import forms

class LoginLogoutForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class' : 'name-field'}))
    password = forms.CharField(max_length=128, label="Password", widget=forms.PasswordInput(attrs={'class' : 'pwd-field'}))


class SignUpForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class' : 'name-field'}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class' : 'email-field'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'pwd-field'}))
    forgot_password = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class' : 'forgot-pwd-checkbox'}))

class OTPVerificationForm(forms.Form):
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'class' : 'email-field'}))
    OTP = forms.CharField(max_length=6, widget=forms.TextInput(attrs={'class' : 'otp-field'}))
