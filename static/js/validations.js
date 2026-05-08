
export function validations(form) {
    const form = document.querySelector('.form');
    let validForm = true;
    /*
    let clientName = form.querySelector('[name="client-name"]').value;
    let clientAddress = form.querySelector('[name="client-address"]').value;
    let clientSSN = form.querySelector('[name="client-ssn"]').value;
    let clientBirth = form.querySelector('[name="client-birth"]').value;
    
    let clientError = form.querySelector('#client-error-msg');
    
    let clientContactItems = form.querySelectorAll('.client-contact-item').value;
    
    let caseStatus = form.querySelector('[name="case-status"]').value;
    let caseAttorney = form.querySelector('[name="attorney-id"]').value;
    let caseAssistant = form.querySelector('[name="assistant-id"]').value;
    
    let caseAdjNum = form.querySelector('[name="case-adj-num"]').value;
    let caseAdjDate = form.querySelector('[name="case-adj-date"]').value;
    
    let caseClaimNum = form.querySelector('[name="case-claim-num"]').value;
    let caseClaimStatus = form.querySelector('[name="case-claim-status"]').value;
    
    let caseSettleDate = form.querySelector('[name="case-settlement-date"]').value;
    
    let injuries = form.querySelectorAll('.injury-item');
    
    let empName = form.querySelector('[name="employer-name"]').value;
    let empAddress = form.querySelector('[name="employer-address"]').value;
    
    let insName = form.querySelector('[name="insurance-name"]').value;
    let insAddress = form.querySelector('[name="insurance-address"]').value;
    
    let cadminName = form.querySelector('[name="claim-admin-name"]').value;
    let cadminAddress = form.querySelector('[name="claim-admin-address"]').value;
    
    let cadjName = form.querySelector('[name="claim-adj-name"]').value;
    
    let cadjContactItems = form.querySelectorAll('.claim-adj-contact-item');
    
    let lfName = form.querySelector('[name="law-firm-name"]').value;
    let lfAddrees = form.querySelector('[name="law-firm-address"]').value;
    
    let dAttName = form.querySelector('[name="def-att-name"]').value;
    let dAsstName = form.querySelector('[name="def-asst-name"]').value;
    
    let dAsstContactItems = form.querySelectorAll('.def-asst-contact-item');
    
    console.log(clientName);
    
    if (clientName.trim() === "" || clientAddress.trim() === "" || 
    clientBirth.trim() === "") {
        
    console.log("validando");
    activateTab("1"); 
        clientError.classList.add('active');
        validForm = false;
    }
    
    let validForm = true;
    */
    
    if (validForm) {
        form.submit();
    }
    else {
        console.log("formulario invalido");
    }
}