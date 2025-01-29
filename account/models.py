from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER,BLOOD_GROUP
# Create your models here.

class UserAccount(models.Model):
    user_account = models.ForeignKey(User,on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12)
    address = models.CharField(max_length=150)
    gender = models.CharField(choices=GENDER,max_length=10)
    blood_group = models.CharField(choices=BLOOD_GROUP,max_length=5)
    image = models.ImageField(upload_to='account/images/')
    birth_date = models.DateField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_account.first_name