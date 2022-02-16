from store.models import Shop, Doctor, Service, ServiceDetailsDay,ServiceDetailsDayTime
from customer.models import Appointment
from auth_app.models import User
from rest_framework import serializers
from rest_framework.authtoken.views import Token
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
import datetime

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
        fields = ['id', 'Day']

class ServicedetailDayTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ServiceDetailsDayTime
        fields = ['id', 'Time','Visit_capacity']

class AppointmentSerializer(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField(read_only=True)
    timing = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model  = Appointment
        fields = ['id', 'doctor', 'Customer', 'timing', 'PatientName', 'Age', 'Sex', 'phone', 'Status', 'Rank','day', 'time']

    def get_doctor(self, obj):
        return DoctorSerializer(obj.Service.ServiceDetailsDayID.ServiceID.Doctor).data
    
    def get_timing(self, obj):
        return ServicedetailDayTimeSerializer(obj.Service).data


class PutAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['Status']


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

class GetDoctorSerializer(serializers.ModelSerializer):
    Doctor = DoctorSerializer(read_only=True)
    timing = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Service
        fields = ['Doctor', 'timing']

    def get_timing(self, obj):
        try:
            service = ServiceDetailsDay.objects.get(ServiceID=obj, Day=str(datetime.datetime.today().isoweekday()))
            return ServicedetailDayTimeSerializer(service.serviceDetailsDayTimes.all(), many=True).data

        except ServiceDetailsDay.DoesNotExist:
            return None

# class ViewDoctorSerializer(serializers.ModelSerializer):
#     class Meta:


class HomeSreenSerializer(serializers.ModelSerializer):
    doctors = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ['id', 'Name', 'Shop_owner', 'Image', 'Interior_image', 'Status', 'Shop_url', 'Opening_time', 'Closing_time', 'doctors']

    def get_doctors(self, obj):
        return GetDoctorSerializer(obj.services.all(), many=True).data


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password",),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

class ServiceDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceDetailsDay
        fields = ['Day']

class PutDoctorSerializer(serializers.ModelSerializer):
    visit_days = serializers.SerializerMethodField()
    timings = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['visit_days', 'timings']

    def get_timings(self, obj):
        queryset = ServiceDetailsDayTime.objects.filter(ServiceDetailsDayID__ServiceID=obj)
        return ServicedetailDayTimeSerializer(queryset, many=True)
      
    def get_visit_days(self, obj):
        return ServiceDaysSerializer(obj.serviceDetailsDays.all(), many=True).data
    

class ClinicDoctorSerializer(serializers.Serializer):
    Doctor = DoctorSerializer()
    visit_days = serializers.SerializerMethodField()
    timings = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ['Doctor', 'Fees', 'visit_days', 'timings']
    
    def get_timings(self, obj):
        queryset = ServiceDetailsDayTime.objects.filter(ServiceDetailsDayID__ServiceID=obj)
        return ServicedetailDayTimeSerializer(queryset, many=True).data

    def get_visit_days(self, obj):
        return ServiceDaysSerializer(obj.serviceDetailsDays.all(), many=True).data

