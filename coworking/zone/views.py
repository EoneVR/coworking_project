from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from .models import *
from .serializers import *


# Create your views here.

class RoomView(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        queryset = Room.objects.all()
        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Room.objects.all()
        room = get_object_or_404(queryset, pk=pk)
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    def create(self, request):
        serializer = RoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def update(self, request, pk=None):
        room = get_object_or_404(Room, pk=pk)
        serializer = RoomSerializer(room, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def partial_update(self, request, pk=None):
        room = get_object_or_404(Room, pk=pk)
        serializer = RoomSerializer(room, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=202)

    def delete(self, request, pk=None):
        room = get_object_or_404(Room, pk=pk)
        room.delete()
        return Response({'message': 'Комната удалена'}, status=204)


class TariffView(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        queryset = Tariff.objects.all()
        serializer = TariffSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Tariff.objects.all()
        tariff = get_object_or_404(queryset, pk=pk)
        serializer = TariffSerializer(tariff)
        return Response(serializer.data)

    def create(self, request):
        serializer = TariffSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def update(self, request, pk=None):
        tariff = get_object_or_404(Tariff, pk=pk)
        serializer = TariffSerializer(tariff, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def partial_update(self, request, pk=None):
        tariff = get_object_or_404(Tariff, pk=pk)
        serializer = TariffSerializer(tariff, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=202)

    def delete(self, request, pk=None):
        tariff = get_object_or_404(Tariff, pk=pk)
        tariff.delete()
        return Response({'message': 'Тариф удален'}, status=204)


class BookingView(viewsets.ViewSet):
    permission_classes = [permissions.IsAdminUser]

    def list(self, request):
        queryset = Booking.objects.all()
        serializer = BookingSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Booking.objects.all()
        booking = get_object_or_404(queryset, pk=pk)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    def create(self, request):
        serializer = BookingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    def update(self, request, pk=None):
        booking = get_object_or_404(Booking, pk=pk)
        serializer = BookingSerializer(booking, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    def partial_update(self, request, pk=None):
        booking = get_object_or_404(Booking, pk=pk)
        serializer = BookingSerializer(booking, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=202)

    def delete(self, request, pk=None):
        booking = get_object_or_404(Booking, pk=pk)
        booking.delete()
        return Response({'message': 'Бронь удалена'}, status=204)
