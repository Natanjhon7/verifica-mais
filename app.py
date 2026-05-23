import os
import re
from flask import Flask, request, jsonify
from flask_cors import CORS

# Tenta importar bibliotecas de ML, mas não falha se não tiver
try:
    import pandas as pd
    import joblib
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.naive_bayes import MultinomialNB
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    print("⚠️ Bibliotecas de ML não disponíveis")

app = Flask(__name__)
CORS(app)

# Configurações
PORT = int(os.environ.get("PORT", 10000))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Modelos
model = None
vectorizer = None

def load_models():
    global model, vectorizer
    if not ML_AVAILABLE:
        return False
    
    model_path = os.path.join(BASE_DIR, 'models', 'naive_bayes.pkl')
    vec_path = os.path.join(BASE_DIR, 'models', 'vectorizer.pkl')
    
    try:
        if os.path.exists(model_path):
            model = joblib.load(model_path)
            vectorizer = joblib.load(vec_path)
            print("✅ Modelos carregados com sucesso!")
            return True
        else:
            print(f"❌ Modelo não encontrado em: {model_path}")
            return False
    except Exception as e:
        print(f"❌ Erro ao carregar modelos: {e}")
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
        'ml_disponivel': ML_AVAILABLE and model is not None
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'model_loaded': model is not None if ML_AVAILABLE else False
    })

@app.route('/check', methods=['POST'])
def check():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Requisição inválida'}), 400
        
        claim = data.get('claim', '')
        if not claim:
            return jsonify({'error': 'Digite uma afirmação'}), 400
        
        if model and vectorizer:
            claim_clean = clean_text(claim)
            claim_vec = vectorizer.transform([claim_clean])
            pred = model.predict(claim_vec)[0]
            proba = model.predict_proba(claim_vec)[0]
            
            rating_map = {0: 'Verdadeiro', 1: 'Falso', 2: 'Indeterminado'}
            rating = rating_map.get(pred, 'Indeterminado')
            
            return jsonify({
                'source': 'Machine Learning (Naive Bayes)',
                'claim': claim,
                'rating': rating,
                'confidence': round(max(proba) * 100, 2),
                'disclaimer': '⚠️ Resultado experimental - caráter acadêmico'
            })
        else:
            # Resposta mockada para teste
            return jsonify({
                'source': 'Modo de Demonstração',
                'claim': claim,
                'rating': 'Indeterminado',
                'disclaimer': '⚠️ Modelo em treinamento - resultado simulado'
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Tenta carregar os modelos
print("=" * 50)
print("🚀 Iniciando Algoritmo Ético...")
print(f"📁 Diretório: {BASE_DIR}")
print(f"🔌 Porta: {PORT}")
print(f"📊 ML Disponível: {ML_AVAILABLE}")

if ML_AVAILABLE:
    load_models()

print("=" * 50)

# Para o Render - EXPORTA o app corretamente
application = app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)