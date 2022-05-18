from django.db import models
from store.models import Shop
from users_auth_api.models import User


class PathologicalTest(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    sample_type = models.CharField(max_length=55, null=True, blank=True)
    precautions = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class PathologicalTestDetail(models.Model):
    clinic = models.ForeignKey(Shop, related_name='clinic_name',
        on_delete=models.CASCADE)
    test_name = models.ForeignKey(PathologicalTest, related_name='test_name',
        on_delete=models.PROTECT)
    image = models.ImageField(upload_to='pathological_test_images', blank=True, null=True)
    fees = models.PositiveSmallIntegerField()
    delivery_duration = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return self.test_name.name

class ShopingCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_cart')
    cart_item = models.ForeignKey(PathologicalTest, on_delete=models.CASCADE, related_name='cart_item')
    quantity = models.SmallIntegerField(default=1)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}: {self.quantity} - {self.cart_item}'


class UserOrder(models.Model):
    user =  models.ForeignKey(User,null=True, blank=True ,on_delete=models.CASCADE)
    date_of_order = models.DateField(auto_now=True)
    complete = models.BooleanField(default=False)
    payment_done = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=12, null=True, blank=True)
    total_price = models.FloatField(default=0)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}: {self.date_of_order} - {self.payment_done}'


class Phlebotomist(models.Model):
    clinic = models.ForeignKey(Shop, related_name='phlebotomists',
        on_delete=models.CASCADE)
    name = models.CharField(max_length=135)
    phone_number = models.CharField(max_length=12)

    def __str__(self):
        return self.name


status_choices = [
    ('0', 'Not assigned'),
    ('1', 'Assigned'),
    ('2', 'delivered'),
    ('3', 'Not Delivered'),
    ('4', 'Collected'),
    ('5', 'Not Collected')
]

class OrderDetail(models.Model):
    booking_for = models.CharField(max_length=35)
    pickup_date = models.DateField()
    pickup_from = models.TextField()
    zipcode = models.CharField(max_length=10)
    contact = models.CharField(max_length=12)
    status = status = models.CharField(max_length=1, choices=status_choices, default='0')
    order_id = models.ForeignKey(UserOrder, on_delete=models.CASCADE, related_name='user_order')
    clinic = models.ForeignKey(Shop, null=True, blank=True, related_name='clinic_detail',on_delete=models.CASCADE)
    user =  models.ForeignKey(User,null=True, blank=True ,on_delete=models.CASCADE)
    phlebotomist =  models.ForeignKey(Phlebotomist,null=True, blank=True ,on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=12, null=True, blank=True)
    total_price = models.FloatField(default=0)
    sample_collected_date = models.DateField(null=True, blank=True)
    date_of_order = models.DateField(auto_now=True)
    complete = models.BooleanField(default=False)
    payment_done = models.BooleanField(default=False)
    

    def __str__(self):
        return self.booking_for

