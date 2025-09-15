from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from bookshop.models import Order, OrderItem
from zone.models import Tariff, Subscription, UserSubscription, Booking
from django.db.models import Sum, F, DecimalField, Count, DurationField, ExpressionWrapper, Avg
from django.utils.dateparse import parse_date
from django.db.models.functions import TruncMonth

PaymentStatus = Order.PaymentStatus


# Create your views here.


class AnalyticsBookshopView(viewsets.ViewSet):
    """
    📊 Аналитика книжного магазина (только для администраторов).

    Ожидает параметры:
    - **start_date**: дата начала периода (YYYY-MM-DD)
    - **end_date**: дата конца периода (YYYY-MM-DD)
    - **report_type**: тип отчёта

    Возможные значения `report_type`:
    - **revenue** → Общая выручка за период
    - **orders_count** → Кол-во заказов
    - **top_books** → Топ-5 продаваемых книг
    - **avg_check** → Средний чек
    - **monthly_sales** → Продажи и заказы по месяцам

    Пример запроса:
    ```
    GET /api/analytics/bookshop/?start_date=2025-01-01&end_date=2025-02-01&report_type=revenue
    ```
    """
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        start_date_str = request.query_params.get("start_date")
        end_date_str = request.query_params.get("end_date")
        report_type = request.query_params.get("report_type")

        start_date = parse_date(start_date_str) if start_date_str else None
        end_date = parse_date(end_date_str) if end_date_str else None

        if not start_date or not end_date:
            return Response(
                {"error": "Укажите даты в формате YYYY-MM-DD"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = OrderItem.objects.filter(
            order__placed_at__date__range=[start_date, end_date],
            order__payment_status=Order.PaymentStatus.COMPLETE,
        )

        if report_type == "revenue":
            data = queryset.aggregate(
                total_revenue=Sum(F("quantity") * F("unit_price"), output_field=DecimalField())
            )

        elif report_type == "orders_count":
            count_orders = queryset.values("order").distinct().count()
            data = {"orders_count": count_orders}

        elif report_type == "top_books":
            data = (
                queryset.values("book__title")
                .annotate(total_sold=Sum("quantity"))
                .order_by("-total_sold")[:5]
            )

        elif report_type == "avg_check":
            revenue = (
                    queryset.aggregate(
                        total=Sum(F("quantity") * F("unit_price"), output_field=DecimalField())
                    )["total"]
                    or 0
            )
            count_orders = queryset.values("order").distinct().count() or 1
            data = {"average_check": round(revenue / count_orders, 2)}

        elif report_type == "monthly_sales":
            data = (
                queryset.annotate(month=TruncMonth("order__placed_at"))
                .values("month")
                .annotate(
                    revenue=Sum(F("quantity") * F("unit_price"), output_field=DecimalField()),
                    orders_count=Count("order", distinct=True),
                )
                .order_by("month")
            )

        else:
            return Response({"error": "Неверный тип отчёта"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data)


class AnalyticsCoworkingView(viewsets.ViewSet):
    """
    📊 Аналитика коворкинга (только для администраторов).

    Ожидает параметры:
    - **start_date**: дата начала периода (YYYY-MM-DD)
    - **end_date**: дата конца периода (YYYY-MM-DD)
    - **report_type**: тип отчёта (по умолчанию = revenue)

    Возможные значения `report_type`:
    - **revenue** → Общая выручка
    - **room_usage** → Использование комнат (суммарные часы бронирования по комнатам)
    - **popular_room_types** → Популярные типы комнат
    - **subscriptions_usage** → Статистика использования подписок
    - **avg_duration** → Средняя продолжительность бронирования
    - **monthly_stats** → Бронирования и доход по месяцам

    Пример запроса:
    ```
    GET /api/analytics/coworking/?start_date=2025-01-01&end_date=2025-02-01&report_type=room_usage
    ```
    """
    permissions = [permissions.IsAdminUser]

    def list(self, request):
        start_date = parse_date(request.query_params.get('start_date'))
        end_date = parse_date(request.query_params.get('end_date'))
        report_type = request.query_params.get('report_type', 'revenue')

        queryset = Booking.objects.all()
        if start_date and end_date:
            queryset = queryset.filter(start_time__date__range=[start_date, end_date])

        if report_type == "revenue":
            data = queryset.aggregate(total_revenue=Sum("price"))

        elif report_type == "room_usage":
            duration = ExpressionWrapper(F("end_time") - F("start_time"), output_field=DurationField())
            data = (
                queryset.annotate(duration=duration)
                .values("room__title")
                .annotate(
                    total_hours=Sum(
                        ExpressionWrapper(F("duration") / 3600, output_field=DurationField())
                    )
                )
                .order_by("-total_hours")
            )

        elif report_type == "popular_room_types":
            data = (queryset.values("room__room_type").annotate(bookings=Count("id")).order_by("-bookings"))

        elif report_type == "subscriptions_usage":
            with_sub = queryset.filter(subscription__isnull=False).count()
            without_sub = queryset.filter(subscription__isnull=True).count()
            active_subs = UserSubscription.objects.filter(end_date__gte=start_date).count() if start_date else None
            data = {
                "with_subscription": with_sub,
                "without_subscription": without_sub,
                "active_subscriptions": active_subs,
            }

        elif report_type == "avg_duration":
            duration = ExpressionWrapper(F("end_time") - F("start_time"), output_field=DurationField())
            data = queryset.annotate(duration=duration).aggregate(avg_duration=Avg("duration"))

        elif report_type == "monthly_stats":
            data = (
                queryset.annotate(month=TruncMonth("start_time")).values("month").annotate(
                    bookings=Count("id"),
                    revenue=Sum("price")
                ).order_by("month")
            )

        else:
            return Response({"error": "Неверный тип отчёта"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data)
