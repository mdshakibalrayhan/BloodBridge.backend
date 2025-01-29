from django.db import models
from account.models import UserAccount
from event.models import AllEvent
from .constants import BLOOD_GROUP
# Create your models here.

class Donation(models.Model):
    donor = models.ForeignKey(UserAccount,on_delete=models.CASCADE)
    event = models.ForeignKey(AllEvent,on_delete=models.CASCADE)
    donation_date = models.DateTimeField(auto_now_add=True,null=True)
    donated_blood_group = models.CharField(choices=BLOOD_GROUP,max_length=10)
    request_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Donation by : {self.donor.user_account.first_name}"
