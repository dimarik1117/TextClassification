document.querySelector('#btn-restart').addEventListener('click', function(e) {
    e.preventDefault();
    
    const resultBottom = document.querySelector('.result__bottom');
    
    resultBottom.style.opacity = '0';
    resultBottom.style.transition = 'opacity 0.5s ease-in';
    
    setTimeout(() => {
        resultBottom.style.display = 'none';
    }, 500);
});