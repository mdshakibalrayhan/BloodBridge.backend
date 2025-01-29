from django.db import models
from account.models import UserAccount
from donation.models import Donation
# Create your models here.
class UserProfiles(models.Model):
    user = models.OneToOneField(UserAccount,on_delete=models.CASCADE)
    age = models.IntegerField(blank=True,null=True)
    is_available = models.BooleanField(default=True,null=True)
    last_donation_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"profile of : {self.user.user_account.first_name}"

