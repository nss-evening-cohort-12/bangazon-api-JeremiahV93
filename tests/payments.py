import datetime
import json
from rest_framework import status
from rest_framework.test import APITestCase
from bangazonapi.models import Order, Payment


class PaymentTests(APITestCase):
    def setUp(self) -> None:
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {"username": "steve", "password": "Admin8*", "email": "steve@stevebrownlee.com",
                "address": "100 Infinity Way", "phone_number": "555-1212", "first_name": "Steve", "last_name": "Brownlee"}
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.payment = Payment()
        self.payment.account_number = "111-1111-1111"
        self.payment.create_date = datetime.date.today()
        self.payment.expiration_date = "2024-11-11"
        self.payment.customer_id = 1
        self.payment.merchant_name = "Visa"
        self.payment.save()


    def test_create_payment_type(self):
        """
        Ensure we can add a payment type for a customer.
        """
        # Add product to order
        url = "/paymenttypes"
        data = {
            "merchant_name": "American Express",
            "account_number": "111-1111-1111",
            "expiration_date": "2024-12-31",
            "create_date": datetime.date.today()
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["merchant_name"], "American Express")
        self.assertEqual(json_response["account_number"], "111-1111-1111")
        self.assertEqual(json_response["expiration_date"], "2024-12-31")
        self.assertEqual(json_response["create_date"], str(datetime.date.today()))

    def test_complete_order(self):
        """
        Ensure that an order is completed by adding a payment type
        """
        order = Order()
        order.customer_id = 1
        order.created_date = datetime.date.today()
        order.payment_type = None
        order.save()

        

        data = {
            "payment_type": self.payment.id
        }

        url = f"/orders/{order.id}"
        

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


        test_order = Order.objects.get(pk=order.id)
        test_payment = Payment.objects.get(pk=self.payment.id)
        self.assertEqual(test_order.payment_type, test_payment)

    def test_delete_paymenttype(self):
        url = "/paymenttypes/1"
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
