# File: src/main.py 
"""Main execution script modified for case study dataset"""

import pandas as pd
from data_loader import load_raw_data, preprocess_data
from features import FeatureEngineer
from predict import ProductPredictor
from recommend import ProductRecommender

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Product Recommendation System')
    parser.add_argument('--input', required=True, help='Path to input Excel file')
    parser.add_argument('--output', required=True, help='Output CSV path')
    parser.add_argument('--top-ratio', type=float, 
                       help='Fraction of qualified clients to recommend (default 0.15)')
    parser.add_argument('--top-n', type=int, 
                       help='Exact number of clients to recommend')
    return parser.parse_args()


def run_case_study() -> None: #input_path: str, output_path: str
    args = parse_args()
    """Custom pipeline for the provided dataset"""
    # Load and preprocess data
    print("Loading and preprocessing data...")
    raw_data = load_raw_data(args.input)
    processed_data = preprocess_data(raw_data)
    
    # Feature engineering
    print("Engineering features...")
    engineer = FeatureEngineer()
    features = engineer.transform(processed_data)

    # Make predictions
    print("Generating predictions...")
    predictor = ProductPredictor()
    predictions = predictor.predict(features)
    
    # Generate recommendations
    print("Creating recommendations...")
    recommender = ProductRecommender(top_ratio=args.top_ratio,
        top_n=args.top_n)
    recommendations = recommender.recommend(predictions)
    
    # Save results
    recommendations.to_csv(args.output, index=False)
    print(f"Recommendations saved to {args.output}")

if __name__ == "__main__":
    run_case_study(

    )

        # input_path='../data/DataScientist_CaseStudy_Dataset.xlsx',
        # output_path='../outputs/product_recommendations.csv'