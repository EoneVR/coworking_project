from rest_framework import serializers
from .models import *


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'title', 'room_type', 'capacity', 'description', 'image']


class TariffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tariff
        fields = ['id', 'title', 'price_per_hour', 'room_type']


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'title', 'duration', 'price', 'image']


class UserSubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    is_active = serializers.SerializerMethodField()

    class Meta:
        model = UserSubscription
        fields = ['id', 'user', 'subscription', 'start_date', 'is_active']
        read_only_fields = ['end_date', 'is_active']

    def get_is_active(self, obj):
        return obj.is_active

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user

        subscription_obj = validated_data['subscription']

        active = UserSubscription.objects.filter(user=user, end_date__gte=timezone.now().date()).first()
        if active:
            new_end_candidate = subscription_obj.get_end_date(active.end_date)
            delta = new_end_candidate - active.end_date
            active.end_date = (active.end_date + delta)
            active.save()
            return active

        user_subscription = UserSubscription.objects.create(
            user=user,
            subscription=subscription_obj,
            start_date=validated_data.get('start_date', timezone.now().date())
        )
        user_subscription.save()
        return user_subscription


class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'room', 'start_time', 'end_time', 'subscription', 'price']
        read_only_fields = ['price', 'user']

    def validate(self, data):
        start_time = data['start_time']
        end_time = data['end_time']
        now_dt = timezone.now()

        if start_time < now_dt:
            raise serializers.ValidationError("Нельзя бронировать в прошлом")

        if end_time <= start_time:
            raise serializers.ValidationError("Окончание брони должно быть позже начала")

        duration_hours = (end_time - start_time).total_seconds() / 3600
        if duration_hours > Booking.MAX_HOURS:
            raise serializers.ValidationError(f"Макс. длительность брони — {Booking.MAX_HOURS} часов")

        room = data['room']
        overlaps = Booking.objects.filter(
            room=room,
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        if self.instance:
            overlaps = overlaps.exclude(id=self.instance.id)
        if overlaps.exists():
            raise serializers.ValidationError("Комната уже занята в этот интервал")

        subscription = data.get('subscription')
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if subscription:
            if subscription.user != user:
                raise serializers.ValidationError("Подписка не принадлежит текущему пользователю")
            if not subscription.is_active:
                raise serializers.ValidationError("Переданная подписка не активна")

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        booking = Booking(user=user, **validated_data)
        booking.save()
        return booking

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
