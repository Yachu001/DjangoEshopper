from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from .models import Profile

class user_info_form(forms.ModelForm):
	phone =forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}),required=False)
	adress1 =forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address 1',}),required=False)
	adress2 =forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Address 2',}),required=False)
	city =forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'City',}),required=False)
	zipcode =forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Zip Code',}),required=False)
	state =forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'State',}),required=False)
	country =forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Country',}),required=False)

	class Meta:
		model = Profile
		fields = ('phone','adress1','adress2','city','zipcode','state','country')

class signup_form(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(signup_form, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		#self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''

class user_update_form(UserChangeForm):
	password = None
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email')

	def __init__(self, *args, **kwargs):
		super(user_update_form, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

class user_password_update_form(SetPasswordForm):
	class Meta:
		model =User
		fields = ['new_password1','new_password2']

	def __init__(self, *args, **kwargs):
		super(user_password_update_form, self).__init__(*args, **kwargs)

		self.fields['new_password1'].widget.attrs['class'] = 'form-control'
		self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['new_password1'].label = ''
		self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['new_password2'].widget.attrs['class'] = 'form-control'
		self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['new_password2'].label = ''


	
	