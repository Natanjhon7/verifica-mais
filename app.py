from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import os
import re
import sys

app = Flask(__name__)
CORS(app)

# Caminhos absolutos - agora tudo está na raiz
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'naive_bayes.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'models', 'vectorizer.pkl')

# Variáveis globais
model = None
vectorizer = None

print(f"🔍 Iniciando Algoritmo Ético...")
print(f"📁 Diretório: {BASE_DIR}")

def load_models():
    global model, vectorizer
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            print(f"✅ Modelo carregado de: {MODEL_PATH}")
        else:
            print(f"❌ Modelo não encontrado em: {MODEL_PATH}")
            
        if os.path.exists(VECTORIZER_PATH):
            vectorizer = joblib.load(VECTORIZER_PATH)
            print(f"✅ Vectorizer carregado")
        else:
            print(f"❌ Vectorizer não encontrado")
            
        return model is not None and vectorizer is not None
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def clean_text(text):
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r'[^a-zA-Záâãàéêíóôõúç ]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

@app.route('/')
def home():
    return jsonify({
        'status': 'online',
        'nome': 'Algoritmo Ético',
        'versao': '1.0',
        'modelo': 'carregado' if model else 'nao_carregado'
    })

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'ok',
        'model_loaded': model is not None
    })

@app.route('/check', methods=['POST'])
def check_claim():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Requisição inválida'}), 400
        
        claim = data.get('claim', '')
        if not claim:
            return jsonify({'error': 'Nenhuma afirmação'}), 400
        
        if model and vectorizer:
            claim_clean = clean_text(claim)
            claim_vec = vectorizer.transform([claim_clean])
            prediction = model.predict(claim_vec)[0]
            proba = model.predict_proba(claim_vec)[0]
            
            rating_map = {0: 'Verdadeiro', 1: 'Falso', 2: 'Indeterminado'}
            rating = rating_map.get(prediction, 'Indeterminado')
            
            return jsonify({
                'source': 'ML - Naive Bayes',
                'claim': claim,
                'rating': rating,
                'confidence': round(max(proba) * 100, 2),
                'disclaimer': '⚠️ Resultado experimental'
            })
        else:
            return jsonify({
                'source': 'Erro',
                'claim': claim,
                'rating': 'Indisponível',
                'error': 'Modelo não carregado'
            }), 503
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Carrega os modelos
load_models()

# Para o Render
application = app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)