from django import forms 
from .models import CustomUser

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length = 100,
        widget = forms.TextInput(
            attrs= {
                'type':'text',
                'class':'form-control',
                'placeholder':'Username / Email / Phone'

            }
        )
    )
    password = forms.CharField(max_length = 100,
        widget = forms.PasswordInput(
            attrs = {
                'type':'password',
                'class':'form-control',
                'placeholder':'password'
            }
        )
    )

class SignUpForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.order_fields(['username','email','phone','password','club_name','club_logo','established_at'])
    class Meta:
        model = CustomUser
        exclude = ['groups','user_permissions','is_active','is_superuser','is_staff','date_joined','last_login','details']
        widgets = {
            'username':forms.TextInput(attrs={'type':'text','placeholder':'Username','class':'form-control'}),
            'email':forms.EmailInput(attrs={'type':'email','placeholder':'Email','class':'form-control'}),
            'phone':forms.TextInput(attrs={'type':'text','placeholder':'Phone Number','class':'form-control'}),
            'club_name':forms.TextInput(attrs={'type':'text','placeholder':'Club Name','class':'form-control'}),
            'established_at': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'password':forms.PasswordInput(attrs = {'type':'password','class':'form-control','placeholder':'Enter Password'})
        }
    
