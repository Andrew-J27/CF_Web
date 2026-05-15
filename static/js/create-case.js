// Tom Select initialization

const choices = [
    document.getElementById('tom-select-client'),
    document.getElementById('tom-select-employer'),
    document.getElementById('tom-select-insurance-carrier'),
    document.getElementById('tom-select-claim-administrator'),
    document.getElementById('tom-select-claim-adjuster'),
    document.getElementById('tom-select-defense_law_firm'),
    document.getElementById('tom-select-defense_attorney'),
    document.getElementById('tom-select-defense_assistant')
]

choices.forEach(widget => { 
    if (widget) {
        new TomSelect(widget, {
            create: true, 
        }); 
    }
})
 