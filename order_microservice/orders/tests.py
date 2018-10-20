from django.test import TestCase
from .models import Order
from rest_framework.test import APITestCase

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

class CheckBuyerOrder(APITestCase):

    def setUp(self):
        Order.objects.create(
            fk_buyer = 1,
            fk_product = 1,
            buyer_message = 'Test_Message',
            quantity = 1,
            total_price = 1,
            product_name ='Test_Name')
        Order.objects.create(
            fk_buyer = 2,
            fk_product = 1,
            buyer_message = 'Test_Message',
            quantity = 1,
            total_price = 1,
            product_name ='Test_Name')
        Order.objects.create(
            fk_buyer = 1,
            fk_product = 1,
            buyer_message = 'Test_Message',
            quantity = 1,
            total_price = 1,
            closed = True,
            product_name ='Test_Name')
        Order.objects.create(
            fk_buyer = 2,
            fk_product = 1,
            buyer_message = 'Test_Message',
            quantity = 1,
            total_price = 1,
            closed = True,
            product_name ='Test_Name')

    def test_buyer_orders_with_valid_parms(self):
        request = {'user_id':'1'}
        response = self.client.post('/api/buyer_orders/', request)
        self.assertEqual(response.status_code, 200)

    def test_buyer_orders_with_invalid_parms(self):
        request = {'user_id': 'somethingElse'}
        response = self.client.post('/api/buyer_orders/', request)
        self.assertEqual(response.status_code, 400)

    def test_buyer_orders_with_missing_parms(self):
        request = {'error': 'testing'}
        response = self.client.post('/api/buyer_orders/', request)
        self.assertEqual(response.status_code, 400)
