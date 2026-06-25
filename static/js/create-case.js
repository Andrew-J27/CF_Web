// Tom Select initialization

const choices = [
    'client',
    'employer',
    'insurance-carrier',
    'claim-administrator',
    'claim-adjuster',
    'defense_law_firm', 
    'defense_attorney',
    'defense_assistant', 
]

choices.forEach(tag => { 

    const widget = document.getElementById('tom-select-'+tag);
    const create_fields = document.querySelectorAll('.'+tag+'-field');

    if (widget) {

        const tomSelect = new TomSelect(widget, {
            create: true,  // Permitir crear nuevas opciones
            maxItems: 1,   // Solo una opción seleccionable

            createFilter: (input) => {
                // El input es el texto que escribe el usuario
                return input.trim().length > 0;
            },
            onItemAdd: (value, item) => {
                console.log(create_fields);
                // DETECTAR si es NUEVO (string) o EXISTENTE (numérico)
                const esNuevo = isNaN(parseInt(value));
                
                if (esNuevo) {
                    create_fields.forEach(field => {
                        field.disabled = false;
                        field.parentElement.querySelector('label').classList.remove('disabled');
                    })
                } else {
                    create_fields.forEach(field => {
                        field.disabled = true;
                        field.value = '';
                        field.parentElement.querySelector('label').classList.add('disabled');
                    })
                }
            }
        }); 
    }
});
