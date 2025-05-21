document.addEventListener('DOMContentLoaded', function() {    // Solo ejecutar en las páginas deseadas
    if (window.location.pathname === '/' || window.location.pathname.includes('/products/')) {
        initializeCountdown();
    }
});

function initializeCountdown() {
    const countdownElement = document.getElementById('countdown');
    const storageKey = 'promoCountdown';
    const defaultTime = 24 * 60 + 46; 

    let remainingTime = localStorage.getItem(storageKey);
    
    if (remainingTime === null) {
        remainingTime = defaultTime;
        localStorage.setItem(storageKey, remainingTime);
    } else {
        remainingTime = parseInt(remainingTime);
    }

    // Actualizar contador
    function updateCountdown() {
        const minutes = Math.floor(remainingTime / 60);
        const seconds = remainingTime % 60;
        
        countdownElement.textContent = 
            `00:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        if (remainingTime <= 0) {
            countdownElement.textContent = "¡Oferta terminada!";
            localStorage.removeItem(storageKey);
            return;
        }
        
        remainingTime--;
        localStorage.setItem(storageKey, remainingTime);
        setTimeout(updateCountdown, 1000);
    }

    updateCountdown();
}