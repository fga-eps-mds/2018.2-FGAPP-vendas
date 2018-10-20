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
import json

class OrderList(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

@api_view(["POST"])
def create_order(request):
    fk_product = request.data.get('fk_product')
    fk_buyer = request.data.get('fk_buyer')
    buyer_message = request.data.get('buyer_message')
    quantity = request.data.get('quantity')
    total_price = request.data.get('total_price')

    product_name = request.data.get('product_name')

    if(fk_product == None or fk_buyer == None or quantity == None or total_price == None or product_name == None):
        return Response({'error':'Os campos não podem estar vazios'},status=HTTP_400_BAD_REQUEST)

    try:
        product = Order.objects.create(
            fk_buyer = fk_buyer,
            fk_product = fk_product,
            buyer_message = buyer_message,
            quantity = quantity,
            total_price = total_price,
            product_name = product_name)
        return Response(status=HTTP_200_OK)
    except:
        return Response({'error':'Dados inválidos'},status=HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def user_orders(request):
    product_id = request.data.get('product_id')

    if(product_id == None):
        return Response({'error':'Os campos não podem estar vazios'},status=HTTP_400_BAD_REQUEST)

    try:
        orders = Order.objects.filter(fk_product = product_id).values()
        return Response(orders, status=HTTP_200_OK)
    except:
        return Response({'error':'Dados inválidos'}, status=HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def buyer_orders(request):
    user_id = request.data.get('user_id')

    if(user_id == None):
        error = {'error':'O usuário não foi encontrado.'}
        error = json.dumps(error)
        loaded_error = json.loads(error)
        return Response(data=loaded_error,status=HTTP_400_BAD_REQUEST)

    try:
        buyer_orders = Order.objects.filter(fk_buyer = user_id).values()
        valid_orders = []
        for order in buyer_orders:
            if(not order['closed']):
                valid_orders.append(order)
        return Response(valid_orders, status=HTTP_200_OK)
    except:
        error = {'error': 'Dados inválidos'}
        error = json.dumps(error)
        loaded_error = json.loads(error)
        return Response(data=loaded_error, status=HTTP_400_BAD_REQUEST)
