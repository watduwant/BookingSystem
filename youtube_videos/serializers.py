from rest_framework import serializers
from .models import HtmlVideo, CssVideo, PythonVideo, javascriptVideo, DjangoVideo, AngularVideo, DjangoProjectVideo, AngularProjectsVideo


class HtmlVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HtmlVideo
        fields = '__all__'

class CssVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CssVideo
        fields = '__all__'

class PythonVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PythonVideo
        fields = '__all__'

class javascriptVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = javascriptVideo
        fields = '__all__'

class DjangoVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoVideo
        fields = '__all__'

class AngularVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AngularVideo
        fields = '__all__'

class DjangoProjectVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DjangoProjectVideo
        fields = '__all__'

class AngularProjectsVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AngularProjectsVideo
        fields = '__all__'