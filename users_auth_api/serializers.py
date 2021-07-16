from .models import User, UserProfile
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('customer_id', 'phone_number', 'app_source')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ('url', 'email', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        profile.customer_id = profile_data.get('customer_id', profile.phone_number)
        profile.phone_number = profile_data.get('phone_number', profile.phone_number)
        profile.app_source = profile_data.get('app_source', profile.app_source)
        # profile.permissions = profile_data.get('permissions', profile.permissions)
        # profile.trial_period_days = int(profile_data.get('trial_period_days', profile.trial_period_days))
        # profile.in_app_price_display = int(profile_data.get('in_app_price_display', profile.in_app_price_display))
        # profile.account_opened = profile_data.get('account_opened', profile.account_opened)
        # profile.belongs_to = profile_data.get('belongs_to', profile.belongs_to)
        profile.save()

        return instance




class UserTrialSerializer(serializers.Serializer):
    django_tutorial_subscription = serializers.BooleanField()
    angular_tutorial_subscription = serializers.BooleanField()
    django_project_subscription = serializers.BooleanField()
    angular_project_subscription = serializers.BooleanField()

class UserStockPermissionsSerializer(serializers.Serializer):
    permissions = serializers.CharField()
