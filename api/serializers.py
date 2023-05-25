import datetime

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.authtoken.views import Token
from rest_framework.serializers import ModelSerializer

from api.static_variables import USER_STATUS
from auth_app.models import User
from customer.models import Appointment
from store.models import Shop, Doctor, Service, ServiceDetailsDay, ServiceDetailsDayTime, Phlebotomist, OrderService, \
    Pathological_Test_Service


# class ShopSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Shop
#         fields = ['id', 'Name', 'Shop_owner', 'Address', 'Status', 'OffDay', 'Interior_image', 'Image', 'Opening_time',
#                   'Closing_time', 'Shop_url']


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'Name', 'Experience', 'Specialization', 'Image']


class ServicedetailDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceDetailsDay
        fields = ['id', 'ServiceID', 'Day']


# class ServicedetailListDaySerializer(serializers.ModelSerializer):
#     ServiceID = ServicedetailDaySerializer(read_only=True)
#
#     class Meta:
#         model = ServiceDetailsDay
#         fields = ['id', 'ServiceID', 'Day']


class ServiceDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceDetailsDay
        fields = ['Day']


class ServicedetailDayTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceDetailsDayTime
        fields = ['id', 'ServiceDetailsDayID', 'Time', 'Visit_capacity']


class ServiceDetailDayListTimeSerializer(serializers.ModelSerializer):
    ServiceDetailsDayID = ServiceDaysSerializer(read_only=True)

    class Meta:
        model = ServiceDetailsDayTime
        fields = ['id', 'ServiceDetailsDayID', 'Time', 'Visit_capacity']


class PutAppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['Status']


class OrderServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderService
        fields = '__all__'


class PathoOrdersSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='Order__user')
    contact = serializers.CharField(source='Order__user__shippingAddress__MobileNumber')
    date = serializers.DateField(source='DateAdded')
    location = serializers.SerializerMethodField()
    Test = serializers.CharField(source='PathologicalTestService__Tests')

    class Meta:
        model = OrderService
        fields = ['name', 'contact', 'location', 'status', 'report', 'collected_date', 'Test', 'date']

    def get_location(self, obj):
        address = obj.Order.user.shippingAddress
        return f'{address.FlatName}, {address.StreetName}, {address.AddressType}, {address.pincode}'


class PathologicalTestServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pathological_Test_Service
        fields = '__all__'


class ShopSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'Name', 'Shop_owner', 'Address', 'Status', 'OffDay', 'Interior_image', 'Image', 'Opening_time',
                  'Closing_time', 'Shop_url']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'profile_pic', 'mobile', 'status', 'city', 'pincode']

        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user


class ShopListSerializer(ModelSerializer):
    Shop_owner = UserSerializer(read_only=True)

    class Meta:
        model = Shop
        fields = ['id', 'Name', 'Shop_owner', 'Address', 'Status', 'OffDay', 'Interior_image', 'Image', 'Opening_time',
                  'Closing_time', 'Shop_url']


# class ServiceSerializer(ModelSerializer):
#
#     Clinic = ShopSerializer()
#     Doctor = DoctorSerializer()
#     class Meta:
#         model = Service
#         fields = ['id', 'Clinic', 'Doctor', 'Fees']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'Clinic', 'Doctor', 'Fees']


class ServiceListSerializer(serializers.ModelSerializer):
    Clinic = ShopListSerializer(read_only=True)
    Doctor = DoctorSerializer(read_only=True)

    class Meta:
        model = Service
        fields = ['id', 'Clinic', 'Doctor', 'Fees']


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
    shop_owner = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    mobile = serializers.SerializerMethodField()

    class Meta:
        model = Shop
        fields = ['id', 'Name', 'user_id', 'shop_owner', 'Image', 'Interior_image', 'Address', 'Status', 'Shop_url',
                  'Opening_time', 'Closing_time', 'doctors', 'Status', 'OffDay', 'mobile']

    def get_mobile(self, obj):
        return obj.Shop_owner.mobile

    def get_user_id(self, obj):
        return obj.Shop_owner.id

    def get_shop_owner(self, obj):
        return obj.Shop_owner.email

    def get_doctors(self, obj):
        return GetDoctorSerializer(obj.services.all(), many=True).data


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password", ),
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


class visitdaysSerializer(serializers.ModelSerializer):
    serviceDetailsDayTimes = ServicedetailDayTimeSerializer(many=True)

    class Meta:
        model = ServiceDetailsDay
        fields = ['id', 'Day', 'serviceDetailsDayTimes']


class PhlebotomistTestsSerializer(serializers.ModelSerializer):
    test = serializers.CharField(source='PathologicalTestService__Tests')
    cost = serializers.CharField(source='PathologicalTestService__Price')

    class Meta:
        model = OrderService
        fields = ['test', 'price']


class PhlebotomistSerializer(serializers.ModelSerializer):
    test = serializers.SerializerMethodField()

    class Meta:
        model = Phlebotomist
        fields = ['id', 'Name', 'PhoneNumber', 'test']

    def get_test(self, obj):
        return PhlebotomistTestsSerializer(
            OrderService.objects.filter(PathologicalTestService__Shop=obj.Shop, Order__paymentDone=True),
            many=True).data


class ClinicDoctorSerializer(serializers.ModelSerializer):
    Doctor = serializers.SerializerMethodField()
    serviceDetailsDays = visitdaysSerializer(many=True)

    class Meta:
        model = Service
        fields = ['id', 'Doctor', 'Fees', 'serviceDetailsDays']

    def get_Doctor(self, obj):
        return DoctorSerializer(obj.Doctor).data

    def update(self, instance, validated_data):
        visit_days_data = validated_data.pop('serviceDetailsDays')
        visit_days = (instance.serviceDetailsDays).all()
        visit_days = list(visit_days)
        instance.Fees = validated_data.get('Fees', instance.Fees)
        instance.save()

        for visit_day_data in visit_days_data:
            visit_day = visit_days.pop(0)
            visit_day.Day = visit_day_data.get('Day', visit_day.Day)
            timings = visit_day.serviceDetailsDayTimes.all()
            timings = list(timings)
            timings_data = visit_day_data.pop('serviceDetailsDayTimes')
            for timing_data in timings_data:
                timing = timings.pop(0)
                timing.Time = timing_data.get('Time', timing.Time)
                timing.Visit_capacity = timing_data.get('Visit_capacity', timing.Visit_capacity)
                timing.save()

            visit_day.save()

        return instance


class AppointmentServicesSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(source='ServiceID.Doctor')
    timing = ServicedetailDayTimeSerializer(source='serviceDetailsDayTimes', many=True)

    class Meta:
        model = ServiceDetailsDay
        depth = 1
        fields = ['id', 'Day', 'timing', 'doctor']


class AppointmentSerializer(WritableNestedModelSerializer):
    doctor = serializers.SerializerMethodField(read_only=True)
    timing = serializers.SerializerMethodField(read_only=True)
    user_data = UserSerializer(allow_null=True, required=False)
    user_code = serializers.CharField(
        source='appointment_user',
        required=False
    )

    def validate(self, attrs):
        requests = self.context.get('request')
        token_user = requests.user
        if token_user.status == USER_STATUS.SO and not requests.data.get('user_data'):
            raise serializers.ValidationError(
                {"error": "Please provide user information."}
            )
        elif token_user.status == USER_STATUS.CR and requests.data.get('user_data'):
            raise serializers.ValidationError(
                {"error": "Please Don't added any extra stuff."}
            )

        else:
            attrs['token_user'] = token_user
        return attrs

    def create(self, validated_data):
        if validated_data.get('user_data'):
            user_data = validated_data.pop('user_data')
            if user_data:
                user_serializer = UserSerializer(data=user_data)
                user_serializer.is_valid(raise_exception=True)
                user = user_serializer.save()
                if user:
                    print("user create")
        validated_data['appointment_user'] = validated_data.pop('token_user')
        instance = Appointment.objects.create(**validated_data)
        return instance

    class Meta:
        model = Appointment
        fields = [
            'id', 'user_code', 'user_data',
            'Service', 'PatientName', 'Age',
            'Sex', 'phone', 'Status', 'day',
            'time', 'doctor', 'timing'
        ]

    def get_doctor(self, obj):
        return DoctorSerializer(obj.Service.ServiceDetailsDayID.ServiceID.Doctor).data

    def get_timing(self, obj):
        return ServicedetailDayTimeSerializer(obj.Service).data


class AppointmentListSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    Service = ServicedetailDayTimeSerializer(read_only=True)
    appointment_user = UserSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = '__all__'

# {
#     "serviceDetailsDays": [
#         {
#             "Day": "3",
#             "serviceDetailsDayTimes": [
#                 {
#                     "id": 3,
#                     "Time": "09:00:00",
#                     "Visit_capacity": 30
#                 },
#                 {
#                     "id": 4,
#                     "Time": "14:00:00",
#                     "Visit_capacity": 20
#                 },
#                 {
#                     "id": 5,
#                     "Time": "18:00:00",
#                     "Visit_capacity": 20
#                 }
#             ]
#         },
#         {
#             "id": 1,
#             "Day": "4",
#             "serviceDetailsDayTimes": [
#                 {
#                     "id": 1,
#                     "Time": "09:00:00",
#                     "Visit_capacity": 18
#                 },
#                 {
#                     "id": 2,
#                     "Time": "12:00:00",
#                     "Visit_capacity": 50
#                 }
#             ]
#         }
#     ],
#     "Fees": 700
# }
