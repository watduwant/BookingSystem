# from .models import StockTip, GenericNotification
from rest_framework import serializers


# class StockTipsSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = StockTip
#         fields = ('stock_tip_datetime', 'type', 'category', 'description', 'note', 'note_datetime', 'target_achieved', 'target_achieved_datetime')


# class GenericNotificationSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = GenericNotification
#         fields = ('notification_body', 'notification_datetime')