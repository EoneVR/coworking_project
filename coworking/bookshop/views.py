from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from .models import Category, Book, Cart, CartItem
from .serializers import CategorySerializer, BookSerializer, CartSerializer, CartItemSerializer, \
    OrderSerializer, OrderItemSerializer
from .permissions import CustomPermission
from .services.orders import OrderService
from .services.payments import PaymentService


# Create your views here.
class CategoryView(viewsets.ViewSet):
    permission_classes = [CustomPermission]

    def list(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Category.objects.all()
        category = get_object_or_404(queryset, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def update(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def destroy(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response({'message': 'Категория удалена'}, status=204)

    @action(detail=True, methods=['get'], url_path='books')
    def get_book_by_category(self, request, pk=None):
        book = Book.objects.filter(category_id=pk)
        if not book.exists():
            return Response({'message': 'В данной категории книг нет'}, status=204)
        serializer = BookSerializer(book, many=True)
        return Response(serializer.data)


class BookView(viewsets.ViewSet):
    permission_classes = [CustomPermission]

    def list(self, request):
        queryset = Book.objects.all()
        serializer = BookSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Book.objects.all()
        book = get_object_or_404(queryset, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def create(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def update(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def partial_update(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=202)

    def destroy(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response({"message": "Книга удалена"}, status=204)


class CartView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def _get_cart(self, user):
        cart, _ = Cart.objects.get_or_create(user=user)
        return cart

    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        cart = self._get_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_to_cart(self, request):
        cart = self._get_cart(request.user)
        book_id = request.data.get('book_id')
        quantity = int(request.data.get('quantity', 1))

        if quantity <= 0:
            return Response({'error': 'Количество должно быть больше 0'}, status=400)

        book = get_object_or_404(Book, id=book_id)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=201)

    @action(detail=False, methods=['post'])
    def remove_from_cart(self, request):
        cart = self._get_cart(request.user)
        book_id = request.data.get('book_id')

        if not book_id:
            return Response({'error': 'Книга не найдена'}, status=400)

        cart_item = CartItem.objects.filter(cart=cart, book_id=book_id).first()
        if not cart_item:
            return Response({'error': 'Товар не найден в корзине'}, status=404)

        cart_item.delete()
        return Response({'message': 'Товар удален из корзины'}, status=200)

    @action(detail=False, methods=['post'])
    def clear_cart(self, request):
        cart = self._get_cart(request.user)
        cart.items.all().delete()
        return Response({'message': 'Корзина очищена'}, status=200)


class OrderViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        """Оформление заказа"""
        try:
            order = OrderService.create_order_from_cart(request.user, request.data.get("cart_id"))
        except ValueError as e:
            return Response({"detail": str(e)}, status=400)

        session = PaymentService.create_checkout_session(order)
        serializer = OrderSerializer(order)
        return Response(
            {"order": serializer.data, "checkout_url": session.url},
            status=201,
        )
