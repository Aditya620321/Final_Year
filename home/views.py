from django.shortcuts import render
import pandas as pd
from .models import UserActivity, Product
from rest_framework.views import APIView
from rest_framework.response import Response
from .utils import get_cached_recommendations
from .collaborative import *
from .content_based import *
from .serializer import *
from .models import CartItem
from home.models import Cart, Product  # Import from home.models


from django.shortcuts import redirect, render
from .models import Product  # Adjust based on your actual model name
import streamlit as st
import ast
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

def home_view(request):
    # Your home page logic
    return render(request, 'home/home.html')

def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total_price = 0  # Add total price initialization
    

    for product in products:
        quantity = cart[str(product.id)]
        cart_items.append({'product': product, 'quantity': quantity})
        total_price += product.price * quantity  # Add the product price * quantity to total price

    print(f"Total Price: {total_price}")  # Add this for debugging

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,  # Pass the total price to template
        'MEDIA_URL': settings.MEDIA_URL,
    })


def update_cart(request, product_id):
    cart = request.session.get('cart', {})

    if product_id in cart:
        # Example: Decrease the quantity by 1
        if cart[product_id] > 1:
            cart[product_id] -= 1
        else:
            cart.pop(product_id)  # Remove product if quantity becomes 0

    request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request, product_id):
    # Get the current cart from the session
    cart = request.session.get('cart', {})

    # Remove the product from the cart if it exists
    if str(product_id) in cart:
        del cart[str(product_id)]

    # Save the updated cart back to the session
    request.session['cart'] = cart

    # Redirect the user to the cart page after removal
    return redirect('cart')

from django.shortcuts import render
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

def checkout(request):
    cart = request.session.get('cart', {})
    total_price = 0
    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        total_price += product.price * quantity

    amount_paise = int(total_price * 100)  # Razorpay expects amount in paise

    # Create Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    # Create order
    payment = client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "payment_capture": "1"
    })

    context = {
        "payment": payment,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "total_price": total_price,
    }

    return render(request, "checkout.html", context)


def index(request):
    return render(request, 'index.html')

def product_detail(request, id):
    context = {'id': id}
    return render(request, 'product_detail.html', context)

class LogUserActivity(APIView):
    def get(self, request):
        
        if request.GET.get('product_id') is None:
            return Response({"message": "id required!"}, status=201)

        data = {
            "user"  : request.user.id,
            "product" : request.GET.get('product_id'),
            "action" : "click"
        }
        serializer = UserActivitySerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Automatically set the logged-in user
            activities = UserActivity.objects.filter(user = request.user)
            if activities.count() > 5:
                activities.last().delete()
            return Response({"message": "User activity logged successfully!"}, status=201)
        return Response(serializer.errors, status=200)
    



def get_similar_products_by_user_activity(user_id, top_n=10):
    try:
        user_activities = UserActivity.objects.filter(user_id=user_id)
        if not user_activities.exists():
            return []
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
                similar_product = all_products[idx]
                if similar_product != user_product and similar_product.id not in product_ids:
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

    


class ProductAPI(APIView):
    def get(self, request):
        user_id = request.user.id
        all_products = ProductSerializer(Product.objects.all().order_by('?')[:10], many = True)
        products = get_similar_products_by_user_activity(user_id)
        #products.reverse()
        serializer = ProductSerializer(products, many=True)
        return Response({"all_products" : all_products.data , "similar_products":serializer.data})
    

def get_similar_products(product_id, top_n=10):
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        product_descriptions = Product.objects.all().values_list('description', flat=True)
        tfidf_matrix = vectorizer.fit_transform(product_descriptions)
        target_product = Product.objects.get(id=product_id)
        all_products = list(Product.objects.all())  
        target_index = all_products.index(target_product)
        print(target_index)
        cosine_sim = cosine_similarity(tfidf_matrix[target_index], tfidf_matrix).flatten()
        similar_indices = cosine_sim.argsort()[-top_n-1:-1][::-1]
    
        similar_indices = [i for i in similar_indices if i != target_index]
        print(similar_indices)
        similar_products = []
        for idx in similar_indices:
            similar_product = all_products[idx]  
            print(similar_product)
            if similar_product:  
                similar_products.append(similar_product)

        return similar_products

    except Exception as e:
        import sys
        import os
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno, e)
        return [] 


class ProductDetailAPI(APIView):
    def get(self, request, id):
        product = Product.objects.get(id = id)
        serializer  = ProductSerializer(product)
        products = get_similar_products(id)
        similar_product_serializer = ProductSerializer(products, many=True)
        return Response({"product":serializer.data,"similar_products" : similar_product_serializer.data })
        


def display_products():
    # Load your CSV
    df = pd.read_csv("flipkart_com-ecommerce_sample.csv")

    # Show image and product name
    for index, row in df.iterrows():
        # Display the product name
        st.write(row['product_name'])

        # Convert stringified list to actual list
        try:
            image_list = ast.literal_eval(row['image'])
            if image_list and isinstance(image_list, list):
                st.image(image_list[0], caption=row['product_name'], use_column_width=True)
        except Exception as e:
            st.write("Image could not be loaded.")

# Main Streamlit App
def main():
    st.title('Product Display from CSV')
    display_products()

# Run the app
if __name__ == "__main__":
    main()