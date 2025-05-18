document.getElementById('predict-btn').addEventListener('click', predictCategory);

async function predictCategory() {
    const text = document.getElementById('text-input').value.trim();
    
    if (!text) {
        alert('Пожалуйста, введите текст для классификации');
        return;
    }
    
    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('result').classList.add('hidden');
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        document.getElementById('category').textContent = data.category;
        
        const probabilitiesDiv = document.getElementById('probabilities');
        probabilitiesDiv.innerHTML = '';
        
        const sortedProbabilities = Object.entries(data.probabilities)
            .sort((a, b) => b[1] - a[1]);
        
        sortedProbabilities.forEach(([label, probability]) => {
            const item = document.createElement('div');
            item.className = 'probability-item';
            
            const labelDiv = document.createElement('div');
            labelDiv.className = 'probability-label';
            labelDiv.innerHTML = `
                <span>${label}</span>
                <span>${(probability * 100).toFixed(1)}%</span>
            `;
            
            const bar = document.createElement('div');
            bar.className = 'probability-bar';
            
            const fill = document.createElement('div');
            fill.className = 'probability-fill';
            fill.style.width = `${probability * 100}%`;
            
            bar.appendChild(fill);
            item.appendChild(labelDiv);
            item.appendChild(bar);
            probabilitiesDiv.appendChild(item);
        });
        
        document.getElementById('result').classList.remove('hidden');
    } catch (error) {
        alert('Произошла ошибка: ' + error.message);
        console.error('Error:', error);
    } finally {
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('result').classList.remove('hidden');
    }
}