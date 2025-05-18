document.querySelectorAll('#btn-yes, #btn-no').forEach(button => {
    button.addEventListener('click', function() {
      const resultTop = document.querySelector('.result__top');
      const resultBottom = document.querySelector('.result__bottom');
      
      resultTop.style.opacity = '0';
      resultTop.style.transition = 'opacity 0.5s ease-in';
      
      setTimeout(() => {
        resultTop.style.display = 'none';
        
        resultBottom.style.display = 'flex';
        resultBottom.style.opacity = '0';
        
        setTimeout(() => {
          resultBottom.style.opacity = '1';
          resultBottom.style.transition = 'opacity 0.5s ease-in';
        }, 10);
      }, 500);
    });
  });