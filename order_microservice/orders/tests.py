from django.test import TestCase
from .models import Order
from rest_framework.test import APITestCase
import json
from django.core import serializers
from .serializers import OrderSerializer
from datetime import datetime

class CheckOrderAPITest(APITestCase):

    def test_create_order(self):
        # OK if can create
        request_1 = {'fk_product':'1', 'fk_buyer':'1', 'buyer_message':'Estou no MASP do lado da entrada do RU.', 'quantity':'1', 'total_price':'1.23', 'product_name': 'Bolo no Pote'}
        response_1 = self.client.post('/api/create_order/', request_1)
        self.assertEqual(response_1.status_code, 200)

        # BAD REQUEST if request has not any field
        request_2 = {'fk_product':'1', 'buyer_message':'Estou no MASP do lado da entrada do RU.', 'quantity':'1', 'total_price':'1.23', 'product_name': 'Bolo no Pote'}
        response_2 = self.client.post('/api/create_order/', request_2)
        self.assertEqual(response_2.status_code, 400)

        # BAD REQUEST if some request field does not match
        request_3 = {'fk_product':'Errei', 'fk_buyer':'1', 'buyer_message':'Estou no MASP do lado da entrada do RU.', 'quantity':'1', 'total_price':'1.23', 'product_name': 'Bolo no Pote'}
        response_3 = self.client.post('/api/create_order/', request_3)
        self.assertEqual(response_3.status_code, 400)

    def test_user_orders(self):
        request_1 = {'product_id':'1'}
        response_1 = self.client.post('/api/user_orders/', request_1)
        self.assertEqual(response_1.status_code, 200)

        request_2 = {'product_id':'Errei'}
        response_2 = self.client.post('/api/user_orders/', request_2)
        self.assertEqual(response_2.status_code, 400)

        request_3 = {'error':'testing'}
        response_3 = self.client.post('/api/user_orders/', request_3)
        self.assertEqual(response_3.status_code, 400)

    def test_set_order_status(self):

        #OK if i can set a new status to order
        request_1 = {'fk_product':'1', 'fk_buyer':'1', 'buyer_message':'Estou no MASP do lado da entrada do RU.', 'quantity':'1', 'total_price':'1.23', 'product_name': 'Bolo no Pote'}
        response_1 = self.client.post('/api/create_order/', request_1)

        request_status = {'order_id':'1', 'new_status':'1'}
        response_status = self.client.post('/api/set_order_status/', request_status)
        self.assertEqual(response_status.status_code, 200)

        #BAD REQUEST if the order doesn't exist
        request_2 = {'order_id':'2', 'new_status':'2'}
        response_2 = self.client.post('/api/set_order_status/', request_2)
        self.assertEqual(response_2.status_code, 400)

        #BAD REQUEST if it doesn't give a status or order id
        request_3 = {'new_status':'1'}
        response_3 = self.client.post('/api/set_order_status/', request_3)
        self.assertEqual(response_3.status_code, 400)

        request_4 = {'order_id':'1'}
        response_4 = self.client.post('/api/set_order_status/', request_4)
        self.assertEqual(response_4.status_code, 400)

class CheckBuyerOrder(APITestCase):

    def setUp(self):
        create_new_order(fk_buyer=1)
        create_new_order(fk_buyer=1)
        create_new_order(fk_buyer=2)
        create_new_order(fk_buyer=1, status=1)
        create_new_order(fk_buyer=2, status=1)

    def test_buyer_orders_with_valid_parms(self):
        request = {'user_id':'1'}
        response = self.client.post('/api/buyer_orders/', request)
        self.assertEqual(response.status_code, 200)

        for i in range(0, 1):
            order = Order.objects.all()[i]
            serialized_order, json_order = correct_dates(order, response.data[i])

            self.assertEqual(json_order, serialized_order)

    def test_buyer_orders_with_invalid_parms(self):
        request = {'user_id': 'somethingElse'}
        response = self.client.post('/api/buyer_orders/', request)
        self.assertEqual(response.status_code, 400)

        error = {'error': 'Dados inválidos'}
        error = json.dumps(error)
        loaded_error = json.loads(error)
        self.assertEqual(response.data, loaded_error)

    def test_buyer_orders_with_missing_parms(self):
        request = {'error': 'testing'}
        response = self.client.post('/api/buyer_orders/', request)
        self.assertEqual(response.status_code, 400)

        error = {'error':'O usuário não foi encontrado.'}
        error = json.dumps(error)
        loaded_error = json.loads(error)
        self.assertEqual(response.data, loaded_error)


def correct_dates(order, json_data):
    serialized = OrderSerializer(order).data

    # correcting date pattern to compare dates correctly
    serialized['date'] = order.date.isoformat()
    json_data['date'] = json_data['date'].isoformat()

    return serialized, json_data

def create_new_order(fk_buyer, status=0):

    buyer_message = 'Test Message'
    product_name = 'Test Name'
    fk_product = 1
    quantity = 1
    total_price = 1

    Order.objects.create(
        status = status,
        fk_buyer = fk_buyer,
        fk_product = fk_product,
        buyer_message = buyer_message,
        quantity = quantity,
        total_price = total_price,
        product_name = product_name)
