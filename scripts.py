import django
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'reommend.settings'
django.setup()
import pandas as pd

import random
from faker import Faker
from datetime import datetime
from decimal import Decimal

# Initialize Faker
fake = Faker()
# List of real product names categorized by their respective types
product_data = {
    "Smartphone": [
        ("iPhone 15", "The iPhone 15 offers a powerful chipset and a stunning OLED display, with improved battery life."),
        ("Samsung Galaxy S23", "The Samsung Galaxy S23 offers cutting-edge performance with a vibrant AMOLED display."),
        ("Google Pixel 8", "Google Pixel 8 combines AI-powered camera features with Google's pure Android experience."),
        ("OnePlus 11", "OnePlus 11 brings the latest Qualcomm Snapdragon chipset and a smooth 120Hz AMOLED screen."),
        ("Xiaomi Mi 13", "Xiaomi Mi 13 offers high-end specs at an affordable price, with excellent camera performance.")
    ],
    "Laptop": [
        ("MacBook Pro 16", "MacBook Pro 16 offers outstanding performance, with a Retina display and Apple's M1 Pro chip."),
        ("Dell XPS 13", "Dell XPS 13 provides a compact form factor with high power and a virtually borderless screen."),
        ("HP Spectre x360", "HP Spectre x360 is a convertible laptop with a sleek design and excellent battery life.")
    ],
    "Gaming Console": [
        ("Sony PlayStation 5", "PlayStation 5 offers breathtaking graphics and an immersive gaming experience."),
        ("Microsoft Xbox Series X", "Xbox Series X delivers unmatched power and the best gaming library.")
    ],
    "Tablet": [
        ("Apple iPad Pro", "iPad Pro with Apple M1 chip is perfect for productivity, creativity, and entertainment."),
        ("Samsung Galaxy Tab S9", "Samsung Galaxy Tab S9 offers powerful specs and excellent AMOLED display.")
    ],
    "Headphones": [
        ("Bose QuietComfort 45", "Bose QuietComfort 45 offers superior noise cancellation and amazing sound."),
        ("Sony WH-1000XM5", "Sony WH-1000XM5 provides world-class noise-canceling features with an all-day comfortable fit.")
    ],
    "Smartwatch": [
        ("Apple Watch Ultra", "Apple Watch Ultra is a rugged and durable smartwatch built for extreme environments.")
    ],
    "Camera": [
        ("Canon EOS R5", "Canon EOS R5 offers incredible image quality and powerful video recording capabilities."),
        ("GoPro Hero 11", "GoPro Hero 11 is designed for action enthusiasts, offering 5.3K video capture and HyperSmooth stabilization.")
    ],
    "Graphics Card": [
        ("Nvidia GeForce RTX 4090", "Nvidia RTX 4090 brings outstanding performance and ray tracing for gaming and content creation."),
        ("AMD Ryzen 9 7950X", "AMD Ryzen 9 7950X delivers extreme performance for gaming, multitasking, and rendering.")
    ],
    "Vacuum Cleaner": [
        ("Dyson V15 Detect", "Dyson V15 Detect provides powerful suction and a laser that reveals microscopic dust.")
    ],
    "Grocery": [
        ("Organic Apple", "Fresh and organic apples that are perfect for a healthy snack or in your favorite recipe."),
        ("Fresh Carrot", "Sweet and crunchy carrots, packed with nutrients for a healthy diet."),
        ("Whole Wheat Bread", "Whole wheat bread made with 100% whole grains for a wholesome, nutritious meal."),
        ("Almond Milk", "Creamy and rich almond milk, a great dairy-free alternative to regular milk."),
        ("Eggs (Dozen)", "Fresh eggs from free-range chickens, ideal for cooking and baking."),
        ("Rice (Basmati)", "Premium Basmati rice with a fragrant aroma, perfect for any dish."),
        ("Tomato (Organic)", "Fresh organic tomatoes, packed with flavor and perfect for any recipe."),
        ("Chicken Breast", "Lean and protein-packed chicken breast, ideal for grilling or baking."),
        ("Broccoli", "Fresh and nutritious broccoli, great for salads, stir-fries, and more."),
        ("Bananas", "Sweet and potassium-rich bananas, a perfect snack or smoothie ingredient."),
        ("Milk (1L)", "Fresh milk in 1L packs, a great source of calcium and protein."),
        ("Cucumber", "Crisp and refreshing cucumbers, perfect for salads or as a healthy snack."),
        ("Potatoes", "Fresh potatoes, perfect for boiling, roasting, or making mashed potatoes."),
        ("Green Beans", "Crunchy and fresh green beans, great for stir-fries or as a side dish."),
        ("Onion", "Fresh onions with a sharp flavor, perfect for cooking or garnishing."),
        ("Spinach", "Leafy spinach packed with nutrients, ideal for salads or smoothies."),
        ("Yogurt (Greek)", "Creamy Greek yogurt, rich in protein and probiotics."),
        ("Olive Oil", "High-quality olive oil, great for cooking, drizzling, or making dressings."),
        ("Cheddar Cheese", "A rich and sharp cheddar cheese, perfect for sandwiches and cooking."),
        ("Cottage Cheese", "Soft and creamy cottage cheese, perfect for salads or as a snack.")
    ],
    "Lights": [
        ("LED Ceiling Light", "Energy-efficient LED ceiling light perfect for brightening up any room."),
        ("Smart Bulb", "Smart bulb that can be controlled via an app for different light settings."),
        ("Table Lamp", "Stylish table lamp with adjustable brightness for your desk or bedside table.")
    ],
    "Utensils": [
        ("Stainless Steel Spoon", "Durable stainless steel spoon for everyday use."),
        ("Non-stick Frying Pan", "A high-quality frying pan with a non-stick surface for easy cooking."),
        ("Kitchen Knife Set", "Professional kitchen knife set with sharp blades for chopping, slicing, and dicing.")
    ],
    "Garments": [
        ("Men's T-shirt", "Comfortable cotton t-shirt for casual wear."),
        ("Women's Jacket", "Stylish and warm jacket for the winter season."),
        ("Sports Shoes", "High-performance shoes designed for sports and physical activities.")
    ],
    "Electronics": [
        ("Bluetooth Speaker", "Portable Bluetooth speaker with high-quality sound and long battery life."),
        ("Electric Kettle", "Fast-boiling electric kettle with auto-shutoff feature."),
        ("Laptop Charger", "Reliable charger compatible with most laptop brands.")
    ]
}


# List of categories (which now include grocery)
categories = list(product_data.keys())

# Function to generate and insert products into the database
def generate_products():
    products = []   
    for category, items in product_data.items():
        for product_name, description in items:
            print(product_name, category)
            # Generate a fake price (random between 100 and 3000)
            price = round(random.uniform(100, 3000), 2)
            
            # Create product data structure for each product
            product = {
                "name": product_name,
                "description": description,
                "category": category,
                "price": Decimal(price),
                "created_at": datetime.now()
            }
            products.append(product)
    #print(products)
    return products

# Example: Print the first 5 generated products
from home.models import *

def insert_products_into_db(products):
    for product in products:
        print("Created")
        Product.objects.create(
            name=product['name'],
            description=product['description'],
            product_image = "https://cdni.iconscout.com/illustration/premium/thumb/no-product-illustration-download-in-svg-png-gif-file-formats--ecommerce-package-empty-box-online-shopping-pack-e-commerce-illustrations-6632286.png",
            category=product['category'],
            price=product['price'],
            created_at=product['created_at']
        )

# products = Product.objects.all().delete()
# products = generate_products()
# insert_products_into_db(products)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Get all product descriptions
product_descriptions = Product.objects.all().values_list('description', flat=True)

# Vectorize the product descriptions using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(product_descriptions)

# Function to get the most similar products
def get_similar_products(product_id, top_n=10):
    try:
        # Get the product description for the given product_id
        target_product = Product.objects.get(id=product_id)
        
        # Get the index of the target product in the list
        all_products = list(Product.objects.all())  # Convert the QuerySet to a list
        target_index = all_products.index(target_product)

        # Compute cosine similarity
        cosine_sim = cosine_similarity(tfidf_matrix[target_index], tfidf_matrix).flatten()

        # Get the indices of the most similar products
        similar_indices = cosine_sim.argsort()[-top_n-1:-1][::-1]
        
        # Filter out the target product itself from the similar indices
        similar_indices = [i for i in similar_indices if i != target_index]

        # Check if there are any similar products, and return the available ones
        similar_products = []
        for idx in similar_indices:
            similar_product = all_products[idx]  # Access the product from the list of all products
            if similar_product:  # Only append if the product exists
                similar_products.append(similar_product)

        return similar_products

    except Exception as e:
        import sys
        import os
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, e)
        return []  # Return empty list in case of error

# print(get_similar_products(179))


def get_similar_products_by_user_activity(user_id, top_n=10):
    try:
        user_activities = UserActivity.objects.filter(user_id=user_id)
        product_ids = user_activities.values_list('product', flat=True).distinct()
        user_products = Product.objects.filter(id__in=product_ids)
        descriptions = [product.description for product in user_products]
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(descriptions)
        

        all_products = list(Product.objects.all())
        all_product_descriptions = [product.description for product in all_products]
        
        all_tfidf_matrix = tfidf_vectorizer.transform(all_product_descriptions)
        
        similar_products = set()
        
        for i, user_product in enumerate(user_products):
            cosine_sim = cosine_similarity(tfidf_matrix[i], all_tfidf_matrix).flatten()
            similar_indices = cosine_sim.argsort()[-top_n-1:-1][::-1]
            for idx in similar_indices:
                # Directly compare the products in all_products using their IDs
                similar_product = all_products[idx]
                if similar_product != user_product:  # Ensure the product itself is not recommended
                    similar_products.add(similar_product)
        
        # Convert the set of similar products to a list
        similar_products = list(similar_products)
        
        # Step 4: Return the most similar products
        return similar_products
    
    
    except Exception as e:
        import sys
        import os
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, e)
        return []  # Return empty list in case of error
    

import time
# print(get_similar_products_by_user_activity(1))
import csv
csv_file_path = 'flipkart_com-ecommerce_sample.csv'

with open(csv_file_path, mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        try:
            product_name = row['product_name']
            product_image = eval(row['image'])[0]  # First image from list
            description = row['description']
            category = row['product_category_tree'].split('>>')[0].strip('[]"')  # Extract last category
            price = row['retail_price']

            print(
                product_name,
                product_image,
                description,
                category,
                price,
            )
            #time.sleep(1)

            # Create or update product
            Product.objects.update_or_create(
                name=product_name,
                defaults={
                    'product_image': product_image,
                    'description': description,
                    'category': category,
                    'price': price
                }
            )
        except Exception as e:
            print(e)

print("Products imported successfully!")
