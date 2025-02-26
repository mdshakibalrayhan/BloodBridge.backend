from django.contrib import admin
from .models import Donation
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from user_profile.models import UserProfiles
from account.models import UserAccount
class DonationAdmin(admin.ModelAdmin):
    # Specify the fields to display in the admin list view
    list_display = ['donor', 'event', 'donation_date', 'donated_blood_group','request_status']

    def save_model(self, request, obj, form, change):
        
        obj.save()

        if obj.request_status == True:
            email_subject = "Your Donation request was accepted"
            email_body = render_to_string('admin_email.html', {'user' : obj.donor,'event':obj.event})
            
            email = EmailMultiAlternatives(email_subject , '', to=[obj.donor.user_account.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            user_profile = UserProfiles.objects.get(user=UserAccount.objects.get(user_account=request.user))
            user_profile.last_donation_date = obj.event.time
            user_profile.save()


admin.site.register(Donation, DonationAdmin)