const API_URL = 'http://localhost:5000/check';

async function checkClaim() {
    const claimInput = document.getElementById('claimInput');
    const claim = claimInput.value.trim();
    
    if (event) {
        event.preventDefault();
    }

    if (!claim) {
        alert('Por favor, digite uma afirmação para verificar');
        return;
    }
    
    // Mostra loading
    const loadingDiv = document.getElementById('loading');
    const resultDiv = document.getElementById('result');
    const checkBtn = document.getElementById('checkBtn');
    
    loadingDiv.classList.remove('hidden');
    resultDiv.classList.add('hidden');
    checkBtn.disabled = true;
    checkBtn.textContent = '⏳ Verificando...';
    
    try {
        console.log('Enviando requisição para:', API_URL);
        console.log('Afirmação:', claim);
        
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ claim: claim })
        });
        
        console.log('Resposta status:', response.status);
        
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Dados recebidos:', data);
        
        displayResult(data);
        
    } catch (error) {
        console.error('Erro detalhado:', error);
        alert('Erro ao conectar com o servidor. Verifique se o backend está rodando em http://localhost:5000');
        
        // Mostra erro na tela
        resultDiv.classList.remove('hidden');
        document.getElementById('resultIcon').textContent = '❌';
        document.getElementById('resultTitle').textContent = 'Erro de Conexão';
        document.getElementById('claimText').textContent = claim;
        document.getElementById('rating').textContent = 'Erro';
        document.getElementById('source').textContent = 'Não foi possível conectar ao servidor';
        document.getElementById('rating').className = 'rating-badge rating-indeterminado';
        
    } finally {
        loadingDiv.classList.add('hidden');
        checkBtn.disabled = false;
        checkBtn.textContent = '⚡ Verificar';
    }
}

function displayResult(data) {
    console.log('Exibindo resultado:', data);
    
    const resultDiv = document.getElementById('result');
    const ratingSpan = document.getElementById('rating');
    const claimText = document.getElementById('claimText');
    const sourceSpan = document.getElementById('source');
    const confidenceInfo = document.getElementById('confidenceInfo');
    const disclaimer = document.getElementById('disclaimer');
    const urlLink = document.getElementById('urlLink');
    const resultIcon = document.getElementById('resultIcon');
    const resultTitle = document.getElementById('resultTitle');
    
    // Preenche os dados
    claimText.textContent = data.claim || 'N/A';
    sourceSpan.textContent = data.source || 'Desconhecido';
    
    // Define a classificação e estilo
    let rating = data.rating || 'Indeterminado';
    let ratingClass = '';
    let icon = '';
    
    if (rating.toLowerCase().includes('verdadeiro')) {
        ratingClass = 'rating-verdadeiro';
        icon = '✅';
        resultTitle.textContent = 'Afirmação VERDADEIRA';
    } else if (rating.toLowerCase().includes('falso')) {
        ratingClass = 'rating-falso';
        icon = '❌';
        resultTitle.textContent = 'Afirmação FALSA';
    } else {
        ratingClass = 'rating-indeterminado';
        icon = '⚠️';
        resultTitle.textContent = 'Não foi possível determinar';
    }
    
    resultIcon.textContent = icon;
    ratingSpan.textContent = rating;
    ratingSpan.className = `rating-badge ${ratingClass}`;
    
    // Mostra confiança se for do ML
    if (data.confidence) {
        confidenceInfo.innerHTML = `<strong>Confiança:</strong> ${data.confidence}%`;
        confidenceInfo.classList.remove('hidden');
    } else {
        confidenceInfo.classList.add('hidden');
    }
    
    // Mostra disclaimer se for do ML
    if (data.disclaimer) {
        disclaimer.textContent = data.disclaimer;
        disclaimer.classList.remove('hidden');
    } else {
        disclaimer.classList.add('hidden');
    }
    
    // Mostra URL se existir
    if (data.url) {
        urlLink.innerHTML = `<strong>Fonte:</strong> <a href="${data.url}" target="_blank" style="color: #667eea;">Ver original</a>`;
        urlLink.classList.remove('hidden');
    } else {
        urlLink.classList.add('hidden');
    }
    
    // Mostra publisher se existir
    if (data.publisher) {
        const publisherInfo = document.getElementById('publisherInfo');
        if (!publisherInfo) {
            const p = document.createElement('p');
            p.id = 'publisherInfo';
            p.innerHTML = `<strong>Publicado por:</strong> ${data.publisher}`;
            document.querySelector('.result-content').insertBefore(p, document.getElementById('urlLink'));
        } else {
            publisherInfo.innerHTML = `<strong>Publicado por:</strong> ${data.publisher}`;
            publisherInfo.classList.remove('hidden');
        }
    }
    
    // Mostra o resultado
    resultDiv.classList.remove('hidden');
    
    // Scroll suave para o resultado
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function fillExample(text) {
    const input = document.getElementById('claimInput');
    input.value = text;
    input.focus();
}

// Permitir Ctrl+Enter para enviar
document.getElementById('claimInput').addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        checkClaim();
    }
});

// Testar conexão com o backend ao carregar a página
async function testConnection() {
    try {
        const response = await fetch('http://localhost:5000/health');
        if (response.ok) {
            const data = await response.json();
            console.log('✅ Backend conectado:', data);
            if (!data.model_loaded) {
                console.warn('⚠️ Modelo não carregado no backend');
            }
        }
    } catch (error) {
        console.error('❌ Backend não está rodando:', error);
    }
}

// Previne qualquer comportamento de submit
document.addEventListener('DOMContentLoaded', function() {
    // Previne submit de qualquer formulário
    const forms = document.getElementsByTagName('form');
    for (let form of forms) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            return false;
        });
    }
    
    // Garante que o botão não recarrega
    const checkBtn = document.getElementById('checkBtn');
    if (checkBtn) {
        checkBtn.addEventListener('click', function(e) {
            e.preventDefault();
            return false;
        });
    }
    
    console.log('✅ Sistema protegido contra recarregamento');
});

// Executa o teste de conexão quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    testConnection();
    console.log('📱 Página carregada - Verifica+ pronto para uso');
});