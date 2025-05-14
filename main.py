import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'reommend.settings'
django.setup()
import pandas as pd
from scipy.sparse import coo_matrix
from implicit.als import AlternatingLeastSquares
from home.models import *
import requests
from home.models import Product
from decimal import Decimal

# Function to fetch product data from the API

Product.objects.all().delete()
def fetch_and_store_products():
    url = "https://api.escuelajs.co/api/v1/products"
    response = requests.get(url)
    
    if response.status_code == 200:
        products_data = response.json()
        
        for product in products_data:
            # Extracting data from the API response
            name = product.get("title", "")
            description = product.get("description", "")
            category_name = product.get("category", {}).get("name", "")
            price = Decimal(product.get("price", 0))
            product_image = product.get("images", [])[0] if product.get("images") else ""  # Assuming the first image is the main image

            # Create a new product object and save it to the database
            Product.objects.create(
                name=name,
                description=description,
                category=category_name,
                price=price,
                product_image=product_image
            )
            print(f"Product '{name}' added successfully.")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")

# Run the function to fetch and store the products
fetch_and_store_products()
