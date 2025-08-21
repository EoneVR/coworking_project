from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import *


# Create your views here.

class PromotionView(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        queryset = Promotion.objects.all()
        serializer = PromotionSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Promotion.objects.all()
        promo = get_object_or_404(queryset, pk=pk)
        serializer = PromotionSerializer(promo)
        return Response(serializer.data)

    def create(self, request):
        serializer = PromotionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def update(self, request, pk=None):
        promo = get_object_or_404(Promotion, pk=pk)
        serializer = PromotionSerializer(promo, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def partial_update(self, request, pk=None):
        promo = get_object_or_404(Promotion, pk=pk)
        serializer = PromotionSerializer(promo, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=202)

    def delete(self, request, pk=None):
        promo = get_object_or_404(Promotion, pk=pk)
        promo.delete()
        return Response({'message': 'Скидка удалена'}, status=204)


class CoffeeView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request):
        queryset = Coffee.objects.all()
        serializer = CoffeeSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Coffee.objects.all()
        coffee = get_object_or_404(queryset, pk=pk)
        serializers = CoffeeSerializer(coffee)
        return Response(serializers.data)

    def create(self, request):
        serializer = CoffeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def update(self, request, pk=None):
        coffee = get_object_or_404(Coffee, pk=pk)
        serializer = CoffeeSerializer(coffee, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def partial_update(self, request, pk=None):
        coffee = get_object_or_404(Coffee, pk=pk)
        serializer = CoffeeSerializer(coffee, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=202)

    def delete(self, request, pk=None):
        coffee = get_object_or_404(Coffee, pk=pk)
        coffee.delete()
        return Response({'message': 'Напиток удален'}, status=204)


class BakeryView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request):
        queryset = Bakery.objects.all()
        serializer = BakerySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Bakery.objects.all()
        bakery = get_object_or_404(queryset, pk=pk)
        serializers = BakerySerializer(bakery)
        return Response(serializers.data)

    def create(self, request):
        serializer = BakerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def update(self, request, pk=None):
        bakery = get_object_or_404(Coffee, pk=pk)
        serializer = BakerySerializer(bakery, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def partial_update(self, request, pk=None):
        bakery = get_object_or_404(Bakery, pk=pk)
        serializer = BakerySerializer(bakery, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=202)

    def delete(self, request, pk=None):
        bakery = get_object_or_404(Bakery, pk=pk)
        bakery.delete()
        return Response({'message': 'Позиция удалена'}, status=204)

#
# class BaseCRUDViewSet(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
# class PromotionView(BaseCRUDViewSet):
#     queryset = Promotion.objects.all()
#     serializer_class = PromotionSerializer
#     permission_classes = [permissions.IsAdminUser]
#
# class CoffeeView(BaseCRUDViewSet):
#     queryset = Coffee.objects.all()
#     serializer_class = CoffeeSerializer
#
# class BakeryView(BaseCRUDViewSet):
#     queryset = Bakery.objects.all()
#     serializer_class = BakerySerializer