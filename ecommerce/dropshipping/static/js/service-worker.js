if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/service-worker.js')
    .then(registration => console.log('Service Worker registrado:', registration))
    .catch(error => console.log('Error al registrar Service Worker:', error));
}
