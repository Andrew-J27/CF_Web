export function loadComponent(element, file, referenceElement = null) {
    if (!(element instanceof HTMLElement)) {
        console.error('Se requiere un elemento HTML válido');
        return Promise.reject('Elemento inválido');
    }
    
    // Construye la URL para archivos estáticos
    let url = file;
    if (!file.startsWith('/static/')) {
        url = `/static/components/${file}`;
    }
    
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            return response.text();
        })
        .then(data => {
            if (referenceElement && referenceElement instanceof HTMLElement) {
                referenceElement.insertAdjacentHTML('afterend', data);
            } else {
                element.insertAdjacentHTML('beforeend', data);
            }
            return data;
        })
        .catch(error => {
            console.error(`Error loading ${file}:`, error);
            return Promise.reject(error);
        });
}