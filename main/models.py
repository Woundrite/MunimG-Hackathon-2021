from django.db import models
import datetime

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=10000)
	surname = models.CharField(max_length=10000)
	expenses = models.CharField(max_length=100000, default="")
	transport_expenses = models.CharField(max_length=100000, default="")
	clothing_expenses = models.CharField(max_length=100000, default="")
	food_expenses = models.CharField(max_length=100000, default="")
	electricity_expenses = models.CharField(max_length=100000, default="")
	water_expenses = models.CharField(max_length=100000, default="")
	rent_expenses = models.CharField(max_length=100000, default="")
	misc_expenses = models.CharField(max_length=100000, default="")
	saving_history = models.CharField(max_length=1000000000000, default="")
	savings = models.CharField(max_length=100000, default="")
	monthly_earnings = models.CharField(max_length=100000, default="")
	last_earning_add = models.DateTimeField(default = datetime.datetime.now())
	today = models.DateTimeField(default = datetime.datetime.now())
	email = models.EmailField(max_length=10000)
	password = models.CharField(max_length=1000)
	is_authenticated=models.BooleanField(default=False)

# from django.db import models
# import datetime
# from django.contrib.auth.models import User

# # Create your models here.

# class UserProfile(models.Model):
# 	user = models.OneToOneField(User, on_delete=models.CASCADE)
# 	date_joined =models.DateTimeField(auto_now_add=True)
# 	model_pic = models.ImageField(null=True, blank=True)
# 	user_insta = models.CharField(max_length=30, blank=True)
# 	expenses = 	savings = models.CharField(max_length=100000, default="0")
# 	savings = models.CharField(max_length=100000, default="")
# 	income = models.CharField(max_length=100000, default="")
# 	last_earning_add = models.DateTimeField(default = datetime.datetime.now())
# 	today = models.DateTimeField(default = datetime.datetime.now())


# 	def __str__(self):
# 		return self.user.username
# 	class Meta:
# 		verbose_name_plural = 'Profiles'