from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from .serializers import *
from .models import *
from bookshop.permissions import BookshopPermission
from bookshop.views import StandardPagination


# Create your views here.

class PromotionView(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        cache_key = 'promotions:list'
        data = cache.get(cache_key)
        if not data:
            queryset = Promotion.objects.all()
            serializer = PromotionSerializer(queryset, many=True)
            data = serializer.data
            cache.set(cache_key, data, 60 * 5)
        return Response(data)

    def retrieve(self, request, pk=None):
        cache_key = f'promotions:{pk}'
        data = cache.get(cache_key)
        if not data:
            queryset = Promotion.objects.all()
            promo = get_object_or_404(queryset, pk=pk)
            serializer = PromotionSerializer(promo)
            data = serializer.data
            cache.set(cache_key, data, 60 * 5)
        return Response(data)

    def create(self, request):
        serializer = PromotionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete('promotions:list')
        return Response(serializer.data, status=201)

    def update(self, request, pk=None):
        promo = get_object_or_404(Promotion, pk=pk)
        serializer = PromotionSerializer(promo, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete(f'promotions:{pk}')
        cache.delete('promotions:list')
        return Response(serializer.data, status=200)

    def partial_update(self, request, pk=None):
        promo = get_object_or_404(Promotion, pk=pk)
        serializer = PromotionSerializer(promo, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete(f'promotions:{pk}')
        cache.delete('promotions:list')
        return Response(serializer.data, status=202)

    def destroy(self, request, pk=None):
        promo = get_object_or_404(Promotion, pk=pk)
        promo.delete()
        cache.delete(f'promotions:{pk}')
        cache.delete('promotions:list')
        return Response({'message': 'Скидка удалена'}, status=204)


class CoffeeView(viewsets.ViewSet):
    permission_classes = [BookshopPermission]
    pagination_class = StandardPagination

    def list(self, request):
        cache_key = 'coffee:list'
        data = cache.get(cache_key)
        if not data:
            queryset = Coffee.objects.all()
            paginator = self.pagination_class()
            paginated_qs = paginator.paginate_queryset(queryset, request)
            serializer = CoffeeSerializer(paginated_qs, many=True)
            data = paginator.get_paginated_response(serializer.data).data
            cache.set(cache_key, data, 60 * 5)
        return Response(data)

    def retrieve(self, request, pk=None):
        cache_key = f'coffee:{pk}'
        data = cache.get(cache_key)
        if not data:
            queryset = Coffee.objects.all()
            coffee = get_object_or_404(queryset, pk=pk)
            serializer = CoffeeSerializer(coffee)
            data = serializer.data
            cache.set(cache_key, data, 60 * 5)
        return Response(data)

    def create(self, request):
        serializer = CoffeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete('coffee:list')
        return Response(serializer.data, status=201)

    def update(self, request, pk=None):
        coffee = get_object_or_404(Coffee, pk=pk)
        serializer = CoffeeSerializer(coffee, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete(f'coffee:{pk}')
        cache.delete('coffee:list')
        return Response(serializer.data, status=200)

    def partial_update(self, request, pk=None):
        coffee = get_object_or_404(Coffee, pk=pk)
        serializer = CoffeeSerializer(coffee, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete(f'coffee:{pk}')
        cache.delete('coffee:list')
        return Response(serializer.data, status=202)

    def destroy(self, request, pk=None):
        coffee = get_object_or_404(Coffee, pk=pk)
        coffee.delete()
        cache.delete(f'coffee:{pk}')
        cache.delete('coffee:list')
        return Response({'message': 'Напиток удален'}, status=204)


class BakeryView(viewsets.ViewSet):
    permission_classes = [BookshopPermission]
    pagination_class = StandardPagination

    def list(self, request):
        cache_key = 'bakery:list'
        data = cache.get(cache_key)
        if not data:
            queryset = Bakery.objects.all()
            paginator = self.pagination_class()
            paginated_qs = paginator.paginate_queryset(queryset, request)
            serializer = BakerySerializer(paginated_qs, many=True)
            data = paginator.get_paginated_response(serializer.data).data
            cache.set(cache_key, data, 60 * 5)
        return Response(data)

    def retrieve(self, request, pk=None):
        cache_key = f'bakery:{pk}'
        data = cache.get(cache_key)
        if not data:
            queryset = Bakery.objects.all()
            bakery = get_object_or_404(queryset, pk=pk)
            serializer = BakerySerializer(bakery)
            data = serializer.data
            cache.set(cache_key, data, 60 * 5)
        return Response(data)

    def create(self, request):
        serializer = BakerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete('bakery:list')
        return Response(serializer.data, status=201)

    def update(self, request, pk=None):
        bakery = get_object_or_404(Bakery, pk=pk)
        serializer = BakerySerializer(bakery, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete(f'bakery:{pk}')
        cache.delete('bakery:list')
        return Response(serializer.data, status=200)

    def partial_update(self, request, pk=None):
        bakery = get_object_or_404(Bakery, pk=pk)
        serializer = BakerySerializer(bakery, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete(f'bakery:{pk}')
        cache.delete('bakery:list')
        return Response(serializer.data, status=202)

    def destroy(self, request, pk=None):
        bakery = get_object_or_404(Bakery, pk=pk)
        bakery.delete()
        cache.delete(f'bakery:{pk}')
        cache.delete('bakery:list')
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
