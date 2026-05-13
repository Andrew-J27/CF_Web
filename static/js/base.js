export function show(element) {
    element.classList.add('active');
}

export function hide(element) {
    element.classList.remove('active');
}

export function isActive(element) {
    return element.classList.contains('active')     
}

const inputs = document.querySelectorAll('input');

inputs.forEach(input => {
    input.autocomplete = 'off';
})