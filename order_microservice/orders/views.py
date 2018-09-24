from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.response import Response

@api_view(["POST"])
def create_order(request):
    fk_product = request.data.get('fk_product')
    fk_buyer = request.data.get('fk_buyer')
    buyer_message = request.data.get('buyer_message')
    quantity = request.data.get('quantity')
    total_price = request.data.get('total_price')

    try:
        product = Order.objects.create(
            fk_buyer = fk_buyer,
            fk_product = fk_product,
            buyer_message = buyer_message,
            quantity = quantity,
            total_price = total_price)
        return Response(status=HTTP_200_OK)
    except:
        return Response({'error':'Campos incorretos'},status=HTTP_400_BAD_REQUEST)


class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
