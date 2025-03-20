"""Module for feature engineering and transformation"""

import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler

class FeatureEngineer:
    """Handles all feature transformations using pre-trained encoders"""
    
    def __init__(self):
        self.ohe = joblib.load('encoders/onehot_encoder.joblib')
        self.scaler = joblib.load('scalers/standard_scaler.joblib')
        self.count_cols =['Count_CA', 'Count_SA', 'Count_MF', 'Count_OVD', 'Count_CC', 'Count_CL']
        self.amt_cols = ['ActBal_CA',
                        'ActBal_SA',
                        'ActBal_MF',
                        'ActBal_OVD',
                        'ActBal_CC',
                        'ActBal_CL',
                        'VolumeCred',
                        'VolumeCred_CA',
                        'TransactionsCred',
                        'TransactionsCred_CA',
                        'VolumeDeb',
                        'VolumeDeb_CA',
                        'VolumeDebCash_Card',
                        'VolumeDebCashless_Card',
                        'VolumeDeb_PaymentOrder',
                        'TransactionsDeb',
                        'TransactionsDeb_CA',
                        'TransactionsDebCash_Card',
                        'TransactionsDebCashless_Card',
                        'TransactionsDeb_PaymentOrder']
        
        
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply all feature transformations"""
        df = self._add_log_features(df)
        df = self._apply_log_transforms(df)
        cat_features = self._encode_categorical(df)
        num_features = self._scale_numerical(df)
        return pd.concat([cat_features.reset_index(drop=True),
                         num_features.reset_index(drop=True),
                         df[['Client']+ [f'log_{col}' for col in self.amt_cols]].reset_index(drop=True)], axis=1)
    
    def _add_log_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create log-transformed amount features"""
        for col in self.amt_cols:
            df[f'log_{col}'] = np.log1p(df[col])
        return df
    
    def _apply_log_transforms(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create log1p features for all amount columns"""
        for col in self.amt_cols:
            if col in df.columns:
                df[f'log_{col}'] = np.log1p(df[col])
            else:
                raise ValueError(f"Missing amount column: {col}")
        return df
    
    def _encode_categorical(self, df: pd.DataFrame) -> pd.DataFrame:
        """One-hot encode categorical features"""
        return pd.DataFrame(
            self.ohe.transform(df[['Sex']]),
            columns=self.ohe.get_feature_names_out(['Sex'])
        )
    
    def _scale_numerical(self, df: pd.DataFrame) -> pd.DataFrame:
        """Scale count features"""
        return pd.DataFrame(
            self.scaler.transform(df[self.count_cols]),
            columns=self.count_cols
        )