from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from .serializers import AngularVideoSerializer, DjangoVideoSerializer, HtmlVideoSerializer, CssVideoSerializer, PythonVideoSerializer, javascriptVideoSerializer, DjangoProjectVideoSerializer, AngularProjectsVideo, DjangoProjectVideo, AngularProjectsVideoSerializer
from .models import HtmlVideo, CssVideo, PythonVideo, javascriptVideo, DjangoVideo, AngularProjectsVideo, AngularVideo, DjangoProjectVideo
from rest_framework import viewsets

# Create your views here.


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    


class HtmlVideosViewSet(viewsets.ModelViewSet):
    queryset = HtmlVideo.objects.all()
    serializer_class = HtmlVideoSerializer
    pagination_class = LargeResultsSetPagination


class CssVideoViewSet(viewsets.ModelViewSet):
    queryset = CssVideo.objects.all()
    serializer_class = CssVideoSerializer
    pagination_class = LargeResultsSetPagination

class PythonVideoViewSet(viewsets.ModelViewSet):
    queryset = PythonVideo.objects.all()
    serializer_class = PythonVideoSerializer
    pagination_class = LargeResultsSetPagination

class JavaScriptVideoViewSet(viewsets.ModelViewSet):
    queryset = javascriptVideo.objects.all()
    serializer_class = javascriptVideoSerializer
    pagination_class = LargeResultsSetPagination

class DjangoVideoViewSet(viewsets.ModelViewSet):
    queryset = DjangoVideo.objects.all()
    serializer_class = DjangoVideoSerializer
    pagination_class = LargeResultsSetPagination

class AngularVideoViewSet(viewsets.ModelViewSet):
    queryset = AngularVideo.objects.all()
    serializer_class = AngularVideoSerializer
    pagination_class = LargeResultsSetPagination

class AngularProjectVideoViewSet(viewsets.ModelViewSet):
    queryset = AngularProjectsVideo.objects.all().order_by('-id')
    serializer_class = AngularProjectsVideoSerializer
    pagination_class = LargeResultsSetPagination

class DjangoProjectVideoViewSet(viewsets.ModelViewSet):
    queryset = DjangoProjectVideo.objects.all().order_by('-id')
    serializer_class = DjangoProjectVideoSerializer
    pagination_class = LargeResultsSetPagination