from sklearn.decomposition import TruncatedSVD
import pandas as pd
import sys, os
from .models import UserActivity


def get_interaction_matrix():
    try:
        # Fetching the user activity data from the database
        user_activity = UserActivity.objects.filter(action="view")
        interaction_data = pd.DataFrame(list(user_activity.values("user_id", "product_id", "action")))
        
        # Map actions to numeric values (view = 0, purchase = 1)
        interaction_data['action'] = interaction_data['action'].map({
            'view': 0,   # No significant interaction
            'purchase': 1  # Positive interaction
        })

        # Create a user-product interaction matrix
        interaction_matrix = interaction_data.pivot(index="user_id", columns="product_id", values="action").fillna(0)
        
        # Ensure the interaction matrix has at least two columns (products)
        if interaction_matrix.shape[1] < 2:
            raise ValueError("Insufficient data for SVD: Less than two products.")
        
        return interaction_matrix
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"{exc_type} {fname} {exc_tb.tb_lineno}: {e}")
        return None


def get_recommended_products_svd(user_id, top_n=5):
    try:
        # Get the interaction matrix
        interaction_matrix = get_interaction_matrix()
        
        if interaction_matrix is None:
            return []  # Return empty list if matrix creation failed
        
        # Apply SVD to the interaction matrix
        svd = TruncatedSVD(n_components=50)
        svd_matrix = svd.fit_transform(interaction_matrix)

        # Get the user index in the interaction matrix
        if user_id not in interaction_matrix.index:
            raise ValueError(f"User ID {user_id} not found in interaction matrix.")
        
        user_idx = interaction_matrix.index.get_loc(user_id)
        predicted_ratings = svd_matrix[user_idx]

        # Get the top N product recommendations based on predicted ratings
        recommended_product_indices = predicted_ratings.argsort()[-top_n:][::-1]
        recommended_products = [interaction_matrix.columns[i] for i in recommended_product_indices]
        
        return recommended_products
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"{exc_type} {fname} {exc_tb.tb_lineno}: {e}")
        return []  # Return an empty list in case of errors
