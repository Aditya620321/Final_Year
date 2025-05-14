from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Product
import numpy as np
import sys, os
from sklearn.preprocessing import OneHotEncoder

def get_product_features():
    try:
        # Fetch all products and their descriptions and categories
        products = Product.objects.all()
        descriptions = [product.description for product in products]
        categories = [product.category for product in products]

        # Convert text descriptions to feature vectors using TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english')
        description_vectors = vectorizer.fit_transform(descriptions).toarray()

        # One-hot encoding for product categories
        encoder = OneHotEncoder(sparse_output=False)
        category_vectors = encoder.fit_transform(np.array(categories).reshape(-1, 1))

        # Combine both description and category features
        product_features = np.hstack([description_vectors, category_vectors])
        
        return products, product_features
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"{exc_type} {fname} {exc_tb.tb_lineno}: {e}")
        return [], []

def get_similar_products(product_id, top_n=5):
    try:
        # Get the product features and all products
        products, product_features = get_product_features()

        # Compute cosine similarity between product features
        similarity_matrix = cosine_similarity(product_features)

        # Find the index of the requested product
        product = Product.objects.get(id=product_id)
        product_idx = next(i for i, p in enumerate(products) if p.id == product.id)

        # Get the similarity scores for the product
        similar_scores = similarity_matrix[product_idx]

        # Get the top N most similar products (excluding itself)
        similar_product_indices = similar_scores.argsort()[-top_n-1:-1][::-1]

        # Get the actual product instances from the indices
        similar_products = [products[i] for i in similar_product_indices]

        return similar_products
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"{exc_type} {fname} {exc_tb.tb_lineno}: {e}")
        return []  # Return empty list in case of errors
