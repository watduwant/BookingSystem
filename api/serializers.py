from store.models import Shop, Doctor, Service, ServiceDetails
from customer.models import Appointment
from auth_app.models import Profile
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.views import Token

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Shop
        fields = ['id', 'Name', 'shop_owner', 'Address', 'Status', 'Image', 'opening_time', 'closing_time']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Doctor
        fields = ['id', 'Name', 'Specialization', 'Image']

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Service
        fields = ['id', 'Clinic', 'Doctor', 'day']

class ServicedetailSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ServiceDetails
        fields = ['id', 'ServiceID', 'Time', 'Fees', 'Visit_capacity']

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Appointment
        fields = ['id', 'Customer', 'Service', 'PatientName', 'Age', 'Sex', 'Status', 'Rank','date']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Profile
        fields = ['id', 'email', 'user', 'profile_pic', 'phone', 'status', 'city', 'pincode']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

        extra_kwargs = {'password':{'write_only':True, 'required':True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user