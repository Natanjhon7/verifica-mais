import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

# Download stopwords (primeira execução)
try:
    nltk.data.find('tokenizers/punkt')
except:
    nltk.download('stopwords')
    nltk.download('punkt')

stop_words = set(stopwords.words('portuguese'))

def clean_text(text):
    """Limpa e pré-processa o texto"""
    text = text.lower()
    text = re.sub(r'[^a-zA-Záâãàéêíóôõúç ]', ' ', text)
    words = text.split()
    words = [w for w in words if w not in stop_words and len(w) > 2]
    return ' '.join(words)

def predict_claim(claim, model, vectorizer):
    """Faz predição usando o modelo treinado"""
    claim_clean = clean_text(claim)
    claim_vectorized = vectorizer.transform([claim_clean])
    
    # Obtém a predição e probabilidade
    prediction = model.predict(claim_vectorized)[0]
    probabilities = model.predict_proba(claim_vectorized)[0]
    confidence = max(probabilities) * 100
    
    rating_map = {0: 'Verdadeiro', 1: 'Falso', 2: 'Indeterminado'}
    
    return {
        'rating': rating_map.get(prediction, 'Indeterminado'),
        'confidence': round(confidence, 2)
    }