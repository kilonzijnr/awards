
  
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile,Project,Rating


class RegistrationForm(UserCreationForm):
    """A Form for user registration"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email','username', 'password', 'password2']

        widgets = {
            'first_name':forms.TextInput(attrs = {'class':'form-control names', 'placeholder':"First Name", 'label': 'First Name'}),
            'last_name':forms.TextInput(attrs = {'class':'form-control names', 'placeholder':"Second Name", 'label': 'Sur Name'}),
            'email':forms.TextInput(attrs = {'class':'form-control names', 'placeholder':"Email Address", 'label': 'Email Address'}),
            'username':forms.TextInput(attrs = {'class':'form-control names', 'placeholder':"Username", 'label': 'Username'}),
            'password':forms.PasswordInput(attrs = {'class':'form-control names','type':'password', 'placeholder':"Password", 'label': 'Password'}),
            'confirm_password':forms.PasswordInput(attrs = {'class':'form-control names', 'placeholder':"Confirm Password", 'label': 'Confirm Password'}),
        }
class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email')


class UpdateUserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 'name','profile_photo', 'bio']
        
        
class NewPostForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user', 'post_date']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }        



class ProjectRatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        exclude = ['project','user']