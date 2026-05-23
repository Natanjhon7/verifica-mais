import requests
import json

def search_factcheck(query):
    """
    Consulta a API do Google Fact Check Tools
    """
    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    
    # Você precisa de uma API key (gratuita)
    # Pega em: https://developers.google.com/fact-check/tools/api/authorizing
    API_KEY = "SUA_API_KEY_AQUI"  # <--- SUBSTITUIR
    
    params = {
        'query': query,
        'languageCode': 'pt',
        'key': API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'claims' in data and len(data['claims']) > 0:
            claim = data['claims'][0]
            review = claim.get('claimReview', [{}])[0]
            
            return {
                'rating': review.get('textualRating', 'Não classificado'),
                'publisher': review.get('publisher', {}).get('name', 'Desconhecido'),
                'url': review.get('url', '')
            }
        return None
        
    except Exception as e:
        print(f"Erro na API: {e}")
        return None

# Versão mockada para teste sem API key
def search_factcheck_mock(query):
    """Versão de teste que retorna dados falsos"""
    mock_responses = {
        'urna': {'rating': 'Falso', 'publisher': 'Aos Fatos', 'url': 'https://...'},
        'fraude': {'rating': 'Falso', 'publisher': 'Lupa', 'url': 'https://...'},
        'lula': {'rating': 'Verdadeiro', 'publisher': 'Aos Fatos', 'url': 'https://...'},
    }
    
    for key in mock_responses:
        if key in query.lower():
            return mock_responses[key]
    return None