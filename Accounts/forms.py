from django import forms
from django.contrib.auth import (authenticate,get_user_model,login,logout)

User = get_user_model()

class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

	def clean(self):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		if username and password:
			user = authenticate(username=username,password=password)
			user_qs = User.objects.filter(username=username)
			if user_qs.count() == 0:
				raise forms.ValidationError("The user does not exist")
			if user_qs.count() == 1:
				user = user_qs.first()
			if not user.check_password(password):
				raise forms.ValidationError("Incurrect password")
			if not user.is_active:
				raise forms.ValidationError("This user is no longer active")
		return super(LoginForm,self).clean()



class UserRegistrationForm(forms.ModelForm):
	email = forms.EmailField(label="Email Address")
	email2 = forms.EmailField(label="Confirm Email")
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = User
		fields = [
			"username",
			"email",
			"password",
		]
	def clean(self):
		email = self.cleaned_data.get("email")
		email2 = self.cleaned_data.get("email2")
		if email!=email2:
			raise forms.ValidationError("Emails must match");
		email_qs =User.objects.filter(email=email)
		if email_qs.exists():
			raise forms.ValidationError("This Email is already used")
		return super(UserRegistrationForm,self).clean()
