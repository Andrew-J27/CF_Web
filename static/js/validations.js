const submitBtn = document.querySelector('#btn-submit'); 
const form = document.querySelector('.form');


submitBtn.addEventListener('click', function() { 

    let validForm = false; 
    
    validForm = true;
    
    if (validForm) {
        submitBtn.disabled = true;
        form.submit();
    }
    else {
        console.log("Formulario invalido");
    }
    
}); 