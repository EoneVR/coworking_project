from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from coworking.bookshop.models import Order, OrderItem
from coworking.zone.models import Tariff, Subscription, UserSubscription, Booking
from django.db.models import Sum, F, DecimalField, Count, DurationField, ExpressionWrapper
from django.utils.dateparse import parse_date
from django.db.models.functions import TruncMonth


# Create your views here.


class AnalyticsBookshopView(viewsets.ViewSet):
    permissions = [permissions.IsAdminUser]

    def list(self, request):
        start_date = parse_date(request.query_params.get('start_date'))
        end_date = parse_date(request.query_params.get('end_date'))
        report_type = request.query_params.get('report_type', 'revenue')

        queryset = OrderItem.objects.filter(order_payment_status=PaymentStatus.COMPLETE)

        if start_date and end_date:
            queryset = queryset.filter(order_placed_at__range=[start_date, end_date])

        if report_type == 'revenue':
            data = queryset.aaggregate(total_revenue=Sum(F("quantity") * F("unit_price"), output_field=DecimalField()))

        elif report_type == 'orders_count':
            count_orders = queryset.values('order').distinct().count()
            data = {'orders_count': count_orders}

        elif report_type == 'top_books':
            data = (queryset.values("book__title").annotate(total_sold=Sum("quantity")).order_by("-total_sold")[:5])

        elif report_type == 'avg_check':
            revenue = queryset.aaggregate(
                total=Sum(F("quantity") * F("unit_price"), output_field=DecimalField()))['total'] or 0
            count_orders = queryset.values('order').distinct().count() or 1
            data = {'average_check': round(revenue / count_orders, 2)}

        elif report_type == 'monthly_sales':
            data = (
                queryset.annotate(month=TruncMonth("order__placed_at")).values("month").annotate(
                    revenue=Sum(F("quantity") * F("unit_price"), output_field=DecimalField()),
                    orders_count=Count("order", distinct=True), ).order_by("month")
            )
        else:
            return Response({'error': 'Не верный тип отчета'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(data)


class AnalyticsCoworkingView(viewsets.ViewSet):
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
            data = queryset.annotate(duration=duration).aggregate(avg_duration=Sum("duration") / Count("id"))

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
