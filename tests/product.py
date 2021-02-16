import json
import datetime
from rest_framework import status
from rest_framework.test import APITestCase
from bangazonapi.models import Product, ProductCategory, ProductRating


class ProductTests(APITestCase):
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

        url = "/productcategories"
        data = {"name": "Sporting Goods"}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["name"], "Sporting Goods")

        self.product = Product()
        self.product.name = "Kite"
        self.product.price = 14.99
        self.product.quantity = 60
        self.product.description = "It flies high"
        self.product.category_id = 1
        self.product.location = "Pittsburgh"
        self.product.customer_id = 1
        self.product.save()

    def test_create_product(self):
        """
        Ensure we can create a new product.
        """
        url = "/products"
        data = {
            "name": "Kite",
            "price": 14.99,
            "quantity": 60,
            "description": "It flies high",
            "category_id": 1,
            "location": "Pittsburgh"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["name"], "Kite")
        self.assertEqual(json_response["price"], 14.99)
        self.assertEqual(json_response["quantity"], 60)
        self.assertEqual(json_response["description"], "It flies high")
        self.assertEqual(json_response["location"], "Pittsburgh")

    def test_update_product(self):
        """
        Ensure we can update a product.
        """
        self.test_create_product()

        url = "/products/1"
        data = {
            "name": "Kite",
            "price": 24.99,
            "quantity": 40,
            "description": "It flies very high",
            "category_id": 1,
            "created_date": datetime.date.today(),
            "location": "Pittsburgh"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["name"], "Kite")
        self.assertEqual(json_response["price"], 24.99)
        self.assertEqual(json_response["quantity"], 40)
        self.assertEqual(json_response["description"], "It flies very high")
        self.assertEqual(json_response["location"], "Pittsburgh")

    def test_get_all_products(self):
        """
        Ensure we can get a collection of products.
        """
        self.test_create_product()
        self.test_create_product()
        self.test_create_product()

        url = "/products"

        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), 4)

    def test_delete_product(self):
        """
        Ensure we can delete a product.
        """
        category = ProductCategory()
        category.name =  "Toys"
        category.save()

        product = Product()
        product.customer_id = 1 
        product.name = "Nerf Gun"
        product.price = 24.99
        product.description = "High powered fun"
        product.quantity = 25
        product.category = category
        product.created_date = datetime.date.today()
        product.location = "Nashville"
        product.image_path = ""
        product.save()

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        product_url = f"/products/{product.id}"


        response = self.client.delete(product_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(product_url)
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def test_product_rated(self):
        """
        Ensure a product can be rated and that rating is read correctly
        """

        product_rating = ProductRating()
        product_rating.product = self.product
        product_rating.customer_id = 1
        product_rating.rating = 4
        product_rating.save()

        
        product_rating2 = ProductRating()
        product_rating2.product = self.product
        product_rating2.customer_id = 1
        product_rating2.rating = 2
        product_rating2.save()

        url = F"/products/{self.product.id}"

        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)


        self.assertEqual(json_response["average_rating"], 3)    
