from rest_framework.response import Response
from rest_framework import permissions, viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.core.cache import cache
from .models import Category, Book, Cart, CartItem
from .serializers import CategorySerializer, BookSerializer, CartSerializer, CartItemSerializer, OrderSerializer
from .permissions import BookshopPermission
from .services.orders import OrderService
from .services.payments import PaymentService
from .tasks import send_order_confirmation


# Create your views here.


class StandardPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryView(viewsets.ViewSet):
    permission_classes = [BookshopPermission]
    pagination_class = StandardPagination

    def list(self, request):
        cache_key = 'categories:list'
        data = cache.get(cache_key)
        if not data:
            queryset = Category.objects.all().order_by('id')
            paginator = self.pagination_class()
            paginated_qs = paginator.paginate_queryset(queryset, request)
            serializer = CategorySerializer(paginated_qs, many=True)
            data = paginator.get_paginated_response(serializer.data).data
            cache.set(cache_key, data, 60 * 5)
        return Response(data)

    def retrieve(self, request, pk=None):
        cache_key = f"categories:{pk}"
        data = cache.get(cache_key)
        if not data:
            queryset = Category.objects.all()
            category = get_object_or_404(queryset, pk=pk)
            serializer = CategorySerializer(category)
            data = serializer.data
            cache.set(cache_key, data, 60 * 5)
        return Response(data)

    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete("categories:list")  # сброс кэша списка
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete(f"categories:{pk}")  # сброс кэша конкретной категории
        cache.delete("categories:list")  # сброс кэша списка
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        cache.delete(f"categories:{pk}")
        cache.delete("categories:list")
        return Response({'message': 'Категория удалена'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'], url_path='books')
    def get_book_by_category(self, request, pk=None):
        cache_key = f"categories:{pk}:books"
        data = cache.get(cache_key)

        if not data:
            books = Book.objects.filter(category_id=pk)
            if not books.exists():
                return Response({'message': 'В данной категории книг нет'}, status=status.HTTP_204_NO_CONTENT)

            paginator = self.pagination_class()
            paginated_qs = paginator.paginate_queryset(books, request)
            serializer = BookSerializer(paginated_qs, many=True)
            data = paginator.get_paginated_response(serializer.data).data
            cache.set(cache_key, data, 60 * 5)

        return Response(data)


class BookView(viewsets.ViewSet):
    permission_classes = [BookshopPermission]
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author', 'unit_price', 'year_of_publish', 'in_stock']
    search_fields = ['title', 'author__name', 'description']
    ordering_fields = ['unit_price', 'year_of_publish', 'title']
    ordering = ['title']

    def get_queryset(self):
        return Book.objects.all()

    def filter_queryset(self, request, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(request, queryset, self)
        return queryset

    def list(self, request):
        cache_key = f"books:list:{request.get_full_path()}"
        data = cache.get(cache_key)

        if not data:
            queryset = self.get_queryset()
            queryset = self.filter_queryset(request, queryset)

            paginator = self.pagination_class()
            paginated_qs = paginator.paginate_queryset(queryset, request)
            serializer = BookSerializer(paginated_qs, many=True)
            data = paginator.get_paginated_response(serializer.data).data
            cache.set(cache_key, data, 60 * 5)
        return Response(data)

    def retrieve(self, request, pk=None):
        cache_key = f'books:{pk}'
        data = cache.get(cache_key)
        if not data:
            queryset = self.get_queryset()
            book = get_object_or_404(queryset, pk=pk)
            serializer = BookSerializer(book)
            data = serializer.data
            cache.set(cache_key, data, 60 * 5)
        return Response(data)

    def create(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete('books:list')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete(f'books:{pk}')
        cache.delete('books:list')
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete(f'books:{pk}')
        cache.delete('books:list')
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        cache.delete(f'books:{pk}')
        cache.delete('books:list')
        return Response({"message": "Книга удалена"}, status=status.HTTP_204_NO_CONTENT)


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
            return Response({'error': 'Количество должно быть больше 0'}, status=status.HTTP_400_BAD_REQUEST)

        book = get_object_or_404(Book, id=book_id)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            book=book,
            defaults={"quantity": quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def remove_from_cart(self, request):
        cart = self._get_cart(request.user)
        book_id = request.data.get('book_id')

        if not book_id:
            return Response({'error': 'Книга не найдена'}, status=status.HTTP_400_BAD_REQUEST)

        cart_item = CartItem.objects.filter(cart=cart, book_id=book_id).first()
        if not cart_item:
            return Response({'error': 'Товар не найден в корзине'}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response({'message': 'Товар удален из корзины'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def clear_cart(self, request):
        cart = self._get_cart(request.user)
        cart.items.all().delete()
        return Response({'message': 'Корзина очищена'}, status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        try:
            order = OrderService.create_order_from_cart(request.user, request.data.get("cart_id"))
            send_order_confirmation.delay(order.id)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        session = PaymentService.create_checkout_session(order)
        serializer = OrderSerializer(order)
        return Response(
            {"order": serializer.data, "checkout_url": session.url},
            status=status.HTTP_201_CREATED,
        )
