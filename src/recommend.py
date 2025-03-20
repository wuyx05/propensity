# File: src/recommend.py
"""Module for generating product recommendations"""

import pandas as pd

class ProductRecommender:
    """Generates final product recommendations based on predictions"""
    
    def __init__(self, top_ratio: float = 0.15,top_n: int = None):
        # self.top_ratio = top_ratio
        if top_ratio and top_n:
            raise ValueError("Use either top_ratio or top_n, not both")
            
        self.top_ratio = top_ratio
        self.top_n = top_n
        
    def recommend(self, predictions: pd.DataFrame) -> pd.DataFrame:
        """Generate final recommendations"""
        # Calculate expected revenue
        predictions['Expected_Revenue'] = predictions['Propensity'] * predictions['Revenue']
        
        # Filter and sort candidates
        candidates = predictions[predictions['Propensity'] >= 0.5]
        sorted_candidates = candidates.sort_values('Expected_Revenue', ascending=False)
        
        # Select top recommendations
        if self.top_n is not None:
            n_top = self.top_n
        else:
            # Use 15% as default if no parameters provided
            ratio = self.top_ratio if self.top_ratio is not None else 0.15
            n_top = int(len(candidates) *ratio)
        n_top = min(n_top,len(candidates)) #if required records more than total, retual all candidates
        recommend_df = sorted_candidates.groupby('Client').head(1)[['Client', 'Product']].rename(columns={'Product': 'Recommended_Product'})
        return recommend_df.head(n_top)