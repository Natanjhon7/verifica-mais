import pandas as pd
import os
from datetime import datetime

DATASET_PATH = 'dataset/claims.csv'

def init_dataset():
   
    if not os.path.exists(DATASET_PATH):
        os.makedirs('dataset', exist_ok=True)
        df = pd.DataFrame(columns=['text', 'rating', 'source', 'publisher', 'date'])
        df.to_csv(DATASET_PATH, index=False)

def save_to_dataset(claim, rating, source, publisher):
   
    init_dataset()
    
    new_row = pd.DataFrame([{
        'text': claim,
        'rating': rating,
        'source': source,
        'publisher': publisher,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }])
    
    df = pd.read_csv(DATASET_PATH)
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DATASET_PATH, index=False)
    print(f"Salvo no dataset: {claim[:50]}... -> {rating}")

def load_dataset():
  
    init_dataset()
    return pd.read_csv(DATASET_PATH)