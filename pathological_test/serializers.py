from rest_framework import serializers
from pathological_test.models import PathologicalTestDetail, PathologicalTest, ShopingCart, OrderDetail, UserOrder, Phlebotomist, ClinicDoctor, Clinic


class PathologicalTestSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PathologicalTest
        fields = ('id', 'name', 'description', 'sample_type',
                 'precautions',)  #ClinicDoctor

class ClinicDoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ClinicDoctor
        fields = "__all__"

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Clinic
        fields = "__all__"


class UserOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model  = UserOrder
        fields = "__all__"


class PhlebotomistSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Phlebotomist
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model  = OrderDetail
        fields = "__all__"


class PathologicalTestDetailSerializer(serializers.ModelSerializer):
    test_name = serializers.CharField(source='test_name.name')
    clinic_name = serializers.CharField(source='clinic.Name')

    class Meta:
        model  = PathologicalTestDetail
        fields = ('id', 'test_name', 'clinic_name', 'image', 'fees', 'delivery_duration')


class ShopingCartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model  = ShopingCart
        fields = ('id', 'user', 'cart_item', 'quantity')


class GetShopingCartSerializer(serializers.ModelSerializer):
    cart_item = PathologicalTestDetailSerializer()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model  = ShopingCart
        fields = ('id', 'user', 'cart_item', 'quantity')
