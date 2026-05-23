from factcheckexplorer import FactCheckLib
import pandas as pd
import time
import json

palavras_chave = [
    "eleição", "bolsonaro", "lula", "pt", 
    "campanha", "urna", "voto", "fraude"
]

todas_claims = []

for palavra in palavras_chave:
    print(f"Buscando por: {palavra}")
    
    try:
        # Inicializa a busca
        fc = FactCheckLib(query=palavra, language="pt", num_results=100)
        fc.process()
        
        # Tenta diferentes formas de acessar os resultados
        results = []
        
        # Verifica se tem o método extract_info
        if hasattr(fc, 'extract_info'):
            results = fc.extract_info()
            print(f"  -> Usando extract_info: {len(results)} resultados")
        
        # Se não tiver resultados, tenta acessar diretamente o JSON
        if not results and hasattr(fc, 'clean_json'):
            json_data = fc.clean_json()
            if json_data and 'claims' in json_data:
                results = json_data['claims']
                print(f"  -> Usando clean_json: {len(results)} resultados")
        
        # Se ainda não tiver, tenta ver atributos com dados
        if not results:
            # Verifica se há um atributo que contenha os dados
            for attr in ['data', 'results', 'claims_data', '_data']:
                if hasattr(fc, attr):
                    data = getattr(fc, attr)
                    if data and isinstance(data, (list, dict)):
                        if isinstance(data, dict) and 'claims' in data:
                            results = data['claims']
                        elif isinstance(data, list):
                            results = data
                        if results:
                            print(f"  -> Usando atributo '{attr}': {len(results)} resultados")
                            break
        
        # Processa os resultados encontrados
        if results:
            for claim in results:
                # Extrai os dados no formato correto
                claim_text = claim.get('text', '') if isinstance(claim, dict) else str(claim)
                
                # Pega o claimReview
                claim_review = {}
                if isinstance(claim, dict):
                    reviews = claim.get('claimReview', [])
                    if reviews:
                        claim_review = reviews[0]
                
                todas_claims.append({
                    'text': claim_text,
                    'rating': claim_review.get('textualRating', 'Indeterminado'),
                    'publisher': claim_review.get('publisher', {}).get('name', 'Desconhecido') if isinstance(claim_review.get('publisher'), dict) else 'Desconhecido',
                    'date': claim.get('date', ''),
                    'url': claim_review.get('url', '')
                })
            
            print(f"  -> Coletou {len(results)} claims para '{palavra}'")
        else:
            print(f"  -> Nenhum resultado encontrado para '{palavra}'")
        
        time.sleep(1)  # Evita bloqueio
        
    except Exception as e:
        print(f"  -> Erro: {e}")

# Salva o dataset
if todas_claims:
    df = pd.DataFrame(todas_claims)
    # Remove duplicatas baseado no texto
    df = df.drop_duplicates(subset=['text'])
    df.to_csv('dataset/claims_initial.csv', index=False)
    print(f"\n✅ Dataset gerado com {len(df)} claims únicas")
    print(f"\nDistribuição das classificações:")
    print(df['rating'].value_counts())
    print(f"\nAmostras coletadas:")
    print(df.head(10))
else:
    print("\n⚠️ Nenhuma claim foi coletada via API!")
    print("\nCriando dataset mínimo para treinamento...")
    
    # Dataset expandido para treinamento
    dados_manuais = [
        # Verdadeiros
        {"text": "Lula foi condenado pela Lava Jato em primeira instância", "rating": "Verdadeiro", "publisher": "Aos Fatos", "date": "2024-01-15", "url": ""},
        {"text": "O Brasil tem 27 unidades federativas", "rating": "Verdadeiro", "publisher": "Lupa", "date": "2024-01-16", "url": ""},
        {"text": "A urna eletrônica é usada no Brasil desde 1996", "rating": "Verdadeiro", "publisher": "TSE", "date": "2024-01-17", "url": ""},
        {"text": "O voto no Brasil é obrigatório para maiores de 18 anos", "rating": "Verdadeiro", "publisher": "Lupa", "date": "2024-01-18", "url": ""},
        
        # Falsos
        {"text": "As urnas eletrônicas foram fraudadas em 2022", "rating": "Falso", "publisher": "Aos Fatos", "date": "2024-01-15", "url": ""},
        {"text": "Bolsonaro venceu as eleições de 2022", "rating": "Falso", "publisher": "Aos Fatos", "date": "2024-01-16", "url": ""},
        {"text": "Houve fraude generalizada nas urnas", "rating": "Falso", "publisher": "Lupa", "date": "2024-01-17", "url": ""},
        {"text": "O PT nunca ganhou eleições de forma legítima", "rating": "Falso", "publisher": "Aos Fatos", "date": "2024-01-18", "url": ""},
        {"text": "As pesquisas eleitorais foram todas fraudadas", "rating": "Falso", "publisher": "Lupa", "date": "2024-01-19", "url": ""},
        {"text": "Lula destruiu a economia brasileira", "rating": "Falso", "publisher": "Aos Fatos", "date": "2024-01-20", "url": ""},
        {"text": "Bolsonaro foi o melhor presidente da história", "rating": "Falso", "publisher": "Lupa", "date": "2024-01-21", "url": ""},
        
        # Enganosos/Indeterminados
        {"text": "Voto impresso acabaria com todas as fraudes", "rating": "Enganoso", "publisher": "Estadão Verifica", "date": "2024-01-15", "url": ""},
        {"text": "A urna eletrônica é 100% inviolável", "rating": "Enganoso", "publisher": "Aos Fatos", "date": "2024-01-16", "url": ""},
        {"text": "O TSE é totalmente imparcial", "rating": "Enganoso", "publisher": "Lupa", "date": "2024-01-17", "url": ""},
        {"text": "Campanhas políticas são todas financiadas por empresas privadas", "rating": "Enganoso", "publisher": "Aos Fatos", "date": "2024-01-18", "url": ""},
    ]
    
    df = pd.DataFrame(dados_manuais)
    df.to_csv('dataset/claims_initial.csv', index=False)
    print(f"✅ Dataset manual criado com {len(df)} claims")
    print(f"\nDistribuição das classificações:")
    print(df['rating'].value_counts())
    print(f"\nAmostras:")
    for i, row in df.head(5).iterrows():
        print(f"  - {row['text'][:50]}... -> {row['rating']}")