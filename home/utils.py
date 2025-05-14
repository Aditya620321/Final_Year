# myapp/recommender/utils.py
from django.core.cache import cache
from .collaborative import *
from .content_based import *

def get_cached_recommendations(user_id, product_id, cache_key, top_n=5):
    cached_recommendations = cache.get(cache_key)

    #if cached_recommendations is None:
    recommendations = get_combined_recommendations(user_id, product_id, top_n)
    #    cache.set(cache_key, recommendations, timeout=3600)  # Cache for 1 hour
    return recommendations
    
    return cached_recommendations

def get_combined_recommendations(user_id, product_id, top_n=5):
    content_based_recommendations = get_similar_products(product_id, top_n)
    collaborative_recommendations = get_recommended_products_svd(user_id, top_n)
    content_based_recommendations = content_based_recommendations or []
    collaborative_recommendations = collaborative_recommendations or []

    combined_recommendations = list(set(content_based_recommendations + collaborative_recommendations))
    return combined_recommendations
