from rest_framework import serializers
from .models import UserProfiles
from account.models import UserAccount
from django.conf import settings

class UserProfilesSerializer(serializers.ModelSerializer):
    #user = serializers.StringRelatedField(many=False)
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    phone_number = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    birth_date = serializers.SerializerMethodField()
    blood_group = serializers.SerializerMethodField()
       

    class Meta:
        model = UserProfiles
        fields = [
            'first_name','last_name','age','address',
            'phone_number','is_available','gender',
            'blood_group','image','birth_date'
            ]
    def get_first_name(self, obj):
        # Accessing first_name via the related User model through UserAccount
        return obj.user.user_account.first_name

    def get_last_name(self, obj):
        # Accessing last_name via the related User model through UserAccount
        return obj.user.user_account.last_name

    def get_phone_number(self, obj):
        # Accessing phone_number via the related UserAccount
        return obj.user.phone_number

    def get_address(self, obj):
        # Accessing address via the related UserAccount
        return obj.user.address

    def get_gender(self, obj):
        # Accessing gender via the related UserAccount
        return obj.user.gender



    def get_image(self, obj):
        request = self.context.get('request')
        if obj.user.image:
            # This will create the full absolute URL, either for development or production
            return request.build_absolute_uri(obj.user.image.url) if request else f"{settings.MEDIA_URL}{obj.user.image.url}"
        return None




    def get_birth_date(self, obj):
        # Accessing birth_date via the related UserAccount
        return obj.user.birth_date

    def get_blood_group(self, obj):
        # Accessing blood_group via the related UserAccount
        return obj.user.blood_group
