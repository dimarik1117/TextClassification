document.querySelector('#btn-class').addEventListener('click', function() {
    const resultTop = document.querySelector('.result__top');
    const resultBottom = document.querySelector('.result__bottom');
    
    const bothHidden = 
        (resultTop.style.display === 'none' || window.getComputedStyle(resultTop).display === 'none') &&
        (resultBottom.style.display === 'none' || window.getComputedStyle(resultBottom).display === 'none');
    
    if (bothHidden) {
        resultTop.style.display = 'flex';
        resultTop.style.opacity = '0';
        
        setTimeout(() => {
            resultTop.style.opacity = '1';
            resultTop.style.transition = 'opacity 0.5s ease-in';
        }, 10);
    }
});