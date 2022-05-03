from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated


from pathological_test.models import PathologicalTestDetail, PathologicalTest, ShopingCart, OrderDetail, UserOrder, Phlebotomist
from pathological_test.serializers import PathologicalTestDetailSerializer, PathologicalTestSerializer, ShopingCartSerializer, GetShopingCartSerializer, OrderDetailSerializer, UserOrderSerializer, PhlebotomistSerializer



class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class ShopingCartViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ShopingCartSerializer

    def get_queryset(self):
        queryset = ShopingCart.objects.filter(user=self.request.user)
        return queryset

class UserOrderViewSet(viewsets.ModelViewSet):
    queryset = UserOrder.objects.all()
    serializer_class = UserOrderSerializer

class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = OrderDetailSerializer

    @action(methods=['get'], detail=False, url_path="filter_by_status_and_clinic", url_name="filter_by_status")
    def filter_by_clinic(self, request, *args, **kwargs):
        status = self.request.query_params.get('status', '')
        clinic = self.request.query_params.get('clinic', '')
        queryset = OrderDetail.objects.filter(status=status, clinic=clinic)
        return filter_test(self, queryset)
        

    # @action(methods=['get'], detail=False, url_path="filter_by_test", url_name="filter_by_test")
    # def filter_by_test(self, request, *args, **kwargs):
    #     test_id = self.request.query_params.get('test_id', '')
    #     queryset = PathologicalTest.objects.filter(test_name=int(test_id))
    #     return filter_test(self, queryset)

class PhlebotomistsViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = Phlebotomist.objects.all()
    serializer_class = PhlebotomistSerializer

    @action(methods=['get'], detail=False, url_path="filter_by_clinic", url_name="filter_by_clinic")
    def filter_by_clinic(self, request, *args, **kwargs):
        clinic_id = self.request.query_params.get('clinic_id', '')
        queryset = PhlebotomistSerializer.objects.filter(clinic=int(clinic_id))
        return filter_test(self, queryset)

class GetShopingCartViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    permission_classes = [IsAuthenticated]
    serializer_class = GetShopingCartSerializer

    def get_queryset(self):
        queryset = ShopingCart.objects.filter(user=self.request.user)
        return queryset


class PathologicalTestViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = PathologicalTest.objects.all()
    serializer_class = PathologicalTestSerializer


def filter_test(self, queryset):
    page = self.paginate_queryset(queryset)
    if page is not None:
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    serializer = self.get_serializer(queryset, many=True)
    return Response(serializer.data)


class PathologicalTestDetailsViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = PathologicalTestDetail.objects.all()
    serializer_class = PathologicalTestDetailSerializer
    pagination_class = LargeResultsSetPagination

    @action(methods=['get'], detail=False, url_path="filter_by_clinic", url_name="filter_by_clinic")
    def filter_by_clinic(self, request, *args, **kwargs):
        clinic_id = self.request.query_params.get('clinic_id', '')
        queryset = PathologicalTest.objects.filter(clinic=int(clinic_id))
        return filter_test(self, queryset)
        

    @action(methods=['get'], detail=False, url_path="filter_by_test", url_name="filter_by_test")
    def filter_by_test(self, request, *args, **kwargs):
        test_id = self.request.query_params.get('test_id', '')
        queryset = PathologicalTest.objects.filter(test_name=int(test_id))
        return filter_test(self, queryset)