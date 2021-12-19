# from django import forms
# from django.forms import ModelForm
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

# from .models import UserProfile

# class RegisterForm(UserCreationForm):

# 	class Meta:
# 		model = User
# 		fields = [
# 			'username',
# 			'email',
# 			'password1',
# 			'password2',
# 		]
# 	def clean_email(self):
# 		email = self.cleaned_data.get('email')
# 		username = self.cleaned_data.get('username')
# 		if email and User.objects.filter(email=email).exclude(username=username).exists():
# 			raise forms.ValidationError(u'Email addresses must be unique.')
# 		return email