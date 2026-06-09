import pandas as pd
import joblib
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Záâãàéêíóôõúç ]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

df = pd.read_csv('dataset/claims.csv')
print(f"✅ Dataset carregado: {len(df)} registros")
print(f"\nDistribuição das classes:")
print(df['rating'].value_counts())

df['clean_text'] = df['text'].apply(clean_text)

label_map = {'Verdadeiro': 0, 'Falso': 1, 'Enganoso': 2}
df['label'] = df['rating'].map(label_map)

df = df.dropna()

X = df['clean_text']
y = df['label']

vectorizer = TfidfVectorizer(max_features=1000)
X_vectorized = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized, y, test_size=0.2, random_state=42
)

model = MultinomialNB()
model.fit(X_train, y_train)


y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n📊 Acurácia: {accuracy:.2%}")
print("\n✅ Modelo treinado com sucesso!")

os.makedirs('../models', exist_ok=True)
joblib.dump(model, '../models/naive_bayes.pkl')
joblib.dump(vectorizer, '../models/vectorizer.pkl')
joblib.dump(model, 'models/naive_bayes.pkl')
joblib.dump(vectorizer, 'models/vectorizer.pkl')

print("\n✅ Modelo salvo em 'models/naive_bayes.pkl'")