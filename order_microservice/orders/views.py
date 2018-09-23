from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer

@api_view(["POST"])
def create_order(request):
    fk_product = request.data.get('fk_product')
    fk_buyer = request.data.get('fk_buyer')
    buyer_message = request.data.get('buyer_message')
    quantity = request.data.get('quantity')
    product_price = request.data.get('product_price')

class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
