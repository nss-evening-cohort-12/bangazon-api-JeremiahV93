import sqlite3
from django.shortcuts import render
from bangazonapi.models import Product, ProductCategory, Customer
from bangazonreports.views import Connection

def products_equal_or_less_999(request):
    if request.method == 'GET':

        with sqlite3.connect(Connection.db_path) as conn:
           
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
               SELECT
                p.id,
                p.name,
                p.price,
                p.description,
                p.quantity,
                p.created_date,
                p.location,
                c.name AS category,
                p.customer_id
                                
                FROM bangazonapi_product p 
                JOIN bangazonapi_productcategory c ON c.id = p.category_id
                WHERE p.price <= 999
                ORDER By price DESC 
            """)

        dataset= db_cursor.fetchall()

        products = []
        
        for row in dataset:

            category = ProductCategory.objects.get(name=row["category"])
            customer = Customer.objects.get(pk=row["customer_id"])

            product = Product()
            product.id = row["id"]
            product.category = category
            product.created_date = row["created_date"]
            product.location = row["location"]
            product.price = row["price"]
            product.quantity = row["quantity"]
            product.customer = customer
            product.name = row["name"]
            product.description = row["description"]
            
            products.append(product)

    template = 'products_listed_under_999.html'
    context = {
        "products_under_1000": products
    }

    return render(request, template, context)
