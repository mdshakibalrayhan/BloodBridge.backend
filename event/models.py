from django.db import models
from account.models import UserAccount
from .constants import STATUS,BLOOD_GROUP
# Create your models here.

class AllEvent(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=150)
    blood_group = models.CharField(choices=BLOOD_GROUP,max_length=5,null=True,blank=True)
    creator = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=100)
    time = models.DateTimeField(blank=True,null=True)
    status = models.CharField(choices=STATUS,default='running',max_length=10)

    def __str__(self):
        return self.title