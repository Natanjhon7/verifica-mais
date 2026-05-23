import pandas as pd
import joblib
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Criar dataset manual
print('📊 Criando dataset de treinamento...')

dados = [
    ['Lula foi condenado pela Lava Jato', 'Verdadeiro'],
    ['As urnas eletrônicas foram fraudadas em 2022', 'Falso'],
    ['Bolsonaro venceu as eleições de 2022', 'Falso'],
    ['O voto impresso é mais seguro que a urna eletrônica', 'Enganoso'],
    ['Não houve provas de fraude nas urnas', 'Verdadeiro'],
    ['O Brasil tem 27 unidades federativas', 'Verdadeiro'],
    ['O PT fraudou todas as eleições', 'Falso'],
    ['A urna eletrônica é auditável', 'Verdadeiro'],
    ['As pesquisas eleitorais sempre erram', 'Enganoso'],
    ['Lula destruiu a economia', 'Falso'],
    ['O TSE é um órgão confiável', 'Verdadeiro'],
    ['Voto impresso acabaria com fraudes', 'Enganoso'],
    ['O sistema eleitoral é fraudulento', 'Falso'],
]

df = pd.DataFrame(dados, columns=['text', 'rating'])

# Limpeza simples
df['clean_text'] = df['text'].str.lower()
df['clean_text'] = df['clean_text'].apply(lambda x: re.sub(r'[^a-z ]', ' ', x))

# Mapear rótulos
label_map = {'Verdadeiro': 0, 'Falso': 1, 'Enganoso': 2}
df['label'] = df['rating'].map(label_map)

print(f'✅ Dataset criado com {len(df)} exemplos')
print(df['rating'].value_counts())

# Vetorização
print('🔄 Vetorizando textos...')
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(df['clean_text'])
y = df['label']

# Treinar modelo
print('🤖 Treinando modelo Naive Bayes...')
model = MultinomialNB()
model.fit(X, y)

# Avaliar
y_pred = model.predict(X)
accuracy = (y_pred == y).mean()
print(f'✅ Acurácia no treino: {accuracy:.2%}')

# Salvar modelos
print('💾 Salvando modelos...')

# Salvar na pasta models (fora do backend)
os.makedirs('../models', exist_ok=True)
joblib.dump(model, '../models/naive_bayes.pkl')
joblib.dump(vectorizer, '../models/vectorizer.pkl')

# Salvar também dentro do backend
os.makedirs('models', exist_ok=True)
joblib.dump(model, 'models/naive_bayes.pkl')
joblib.dump(vectorizer, 'models/vectorizer.pkl')

print('✅ Modelo salvo em:')
print('   - ../models/naive_bayes.pkl')
print('   - models/naive_bayes.pkl')
print('\n🎉 Modelo criado com sucesso! Agora pode rodar o app.py')