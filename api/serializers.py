from store.models import Shop, Doctor, Service, ServiceDetailsDay,ServiceDetailsDayTime
from customer.models import Appointment
from auth_app.models import User
from rest_framework import serializers
from rest_framework.authtoken.views import Token

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Shop
        fields = ['id', 'Name', 'Shop_owner', 'Address', 'Status', 'OffDay', 'Interior_image', 'Image', 'Opening_time', 'Closing_time','Shop_url']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Doctor
        fields = ['id', 'Name', 'Experience', 'Specialization', 'Image']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Service
        fields = ['id', 'Clinic', 'Doctor',  'Fees']

class ServicedetailDaySerializer(serializers.ModelSerializer):
    class Meta:
        model  = ServiceDetailsDay
        fields = ['id', 'ServiceID', 'Day']

class ServicedetailDayTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ServiceDetailsDayTime
        fields = ['id', 'ServiceDetailsDayID', 'Time','Visit_capacity']

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Appointment
        fields = ['id', 'Customer', 'Service', 'PatientName', 'Age', 'Sex', 'phone', 'Status', 'Rank','day', 'time']

# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model  = Profile
#         fields = ['id', 'email', 'user', 'profile_pic', 'phone', 'status', 'city', 'pincode']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'profile_pic', 'mobile', 'status', 'city', 'pincode']

        extra_kwargs = {'password':{'write_only':True, 'required':True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user