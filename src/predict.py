"""Prediction module with comprehensive feature validation"""

import pandas as pd
import joblib
import numpy as np
from typing import Dict, List, Set

class ProductPredictor:
    """Handles predictions for multiple products with proper feature validation"""
    
    def __init__(self):
        self.models = self._load_models()
        self.all_required_features = self._get_all_required_features()
        
    def _load_models(self) -> Dict[str, Dict[str, object]]:
        """Load all pretrained models for each product"""
        return {
            product: {
                'propensity': joblib.load(f'models/sale_{product}.joblib'),
                'revenue': joblib.load(f'models/revenue_{product}.joblib')
            }
            for product in ['CC', 'MF', 'CL']
        }
    
    def _get_all_required_features(self) -> Dict[str, Dict[str, List[str]]]:
        """Get feature requirements for all models across all products"""
        features = {}
        for product in self.models:
            features[product] = {
                'propensity': list(self.models[product]['propensity'].feature_names_in_),
                'revenue': list(self.models[product]['revenue'].feature_names_in_)
            }
        return features
    
    def _get_expected_features(self) -> Set[str]:
        """Get union of all features required by any model"""
        all_features = set()
        for product_features in self.all_required_features.values():
            for model_features in product_features.values():
                all_features.update(model_features)
        return all_features

    def predict(self, processed_data: pd.DataFrame) -> pd.DataFrame:
        """Make predictions on processed features"""
        self._validate_input_features(processed_data)
        
        predictions = []
        for product in ['CC', 'MF', 'CL']:
            predictions.append(
                self._create_product_prediction(processed_data, product)
            )
            
        return pd.concat(predictions)
    
    def _validate_input_features(self, data: pd.DataFrame) -> None:
        """Ensure input contains all required features"""
        missing = self._get_expected_features() - set(data.columns)
        if missing:
            raise ValueError(f"Missing required features: {sorted(missing)}")

    def _create_product_prediction(self, data: pd.DataFrame, product: str) -> pd.DataFrame:
        """Generate predictions for a specific product"""
        # Get model-specific features in correct order
        propensity_features = self.all_required_features[product]['propensity']
        revenue_features = self.all_required_features[product]['revenue']
        
        return pd.DataFrame({
            'Client': data['Client'],
            'Product': product,
            'Propensity': self.models[product]['propensity'].predict_proba(data[propensity_features])[:, 1],
            'Revenue': np.exp(self.models[product]['revenue'].predict(data[revenue_features]))
        })