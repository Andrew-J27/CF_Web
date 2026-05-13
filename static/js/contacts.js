class DynamicFormset {
    constructor(options) {
        this.container = options.container;
        this.prefix = options.prefix;
        this.addButton = options.addButton;
        
        this.totalFormsInput = this.container.querySelector(`input[name="${this.prefix}-TOTAL_FORMS"]`);
        this.itemSelector = '.contact-item';
        this.deleteSelfBtnSelector = '.btn-delete-self';
        // Cambio: ahora usamos active checkbox en lugar de DELETE
        this.activeCheckboxSelector = `input[name$="-active"]`;
        
        this.init();
    }

    init() { 
        // Eventos para botones de eliminar (delegación)
        this.container.addEventListener('click', (e) => {
            const deleteButton = e.target.closest(this.deleteSelfBtnSelector);
            if (deleteButton) {
                e.preventDefault();
                this.handleSoftDelete(deleteButton);
            }
        });

        // Eventos para botón de agregar
        if (this.addButton) {
            this.addButton.addEventListener('click', (e) => {
                e.preventDefault();
                this.addNewItem();
            });
        }
    }

    // Cambio: nuevo método para soft delete
    handleSoftDelete(button) {
        const contactItem = button.closest(this.itemSelector);
        if (!contactItem) return;

        const hiddenId = contactItem.querySelector(`input[name^="${this.prefix}-"][name$="-id"]`);
        const isExisting = hiddenId && hiddenId.value !== '';
        
        if (!isExisting) {
            // Elemento nuevo - eliminar del DOM
            const minForms = parseInt(this.container.querySelector(`input[name="${this.prefix}-MIN_NUM_FORMS"]`).value);
            const currentItems = this.container.querySelectorAll(this.itemSelector);

            if (currentItems.length <= minForms) { 
                return;
            }
            contactItem.remove();
            this.reindexAll();
        } else {

            // Elemento existente - toggle del estado active
            const activeCheckbox = contactItem.querySelector(this.activeCheckboxSelector);
            if (activeCheckbox) {
                const isCurrentlyInactive = contactItem.classList.contains('inactive');
                
                if (!isCurrentlyInactive) {
                    // Marcar como inactivo (soft delete)
                    contactItem.classList.add('inactive');
                    activeCheckbox.checked = false; // false = inactivo
                    
                    // Opcional: desactivar campos visualmente
                    contactItem.querySelectorAll('input, select, textarea, button').forEach(field => {
                        if (!field.matches(this.deleteSelfBtnSelector)) {
                            field.readOnly = true;
                        }
                    }); 

                } else {
                    // Reactivar elemento
                    contactItem.classList.remove('inactive');
                    activeCheckbox.checked = true; // true = activo
                    
                    // Reactivar campos
                    contactItem.querySelectorAll('input, select, textarea, button').forEach(field => {
                        field.readOnly = false;
                    }); 
                }
            }
        }
    }

    addNewItem() {
        let newItem;
        let currentTotal = parseInt(this.totalFormsInput.value);
        
        if (currentTotal === 0) {
            newItem = this.createEmptyItem();
        } else {
            const lastItem = this.container.querySelector(this.itemSelector + ':last-of-type');
            if (!lastItem) return;
            newItem = lastItem.cloneNode(true);
            
            // Limpiar valores del clon
            newItem.querySelectorAll('input:not([type="hidden"])').forEach(input => {
                if (input.type === 'checkbox') {
                    input.checked = true; // Por defecto activo
                } else {
                    input.value = '';
                }
            });
            newItem.querySelectorAll('select').forEach(select => {
                select.selectedIndex = 0;
            });
        }
        
        // Asegurar que no tenga clase inactive
        newItem.classList.remove('inactive');
        newItem.style.opacity = '1';
        
        newItem.querySelectorAll('input, select, textarea, button').forEach(field => {
            field.disabled = false;
        });
        
        const newIndex = currentTotal;
        
        // Reemplazar índices
        newItem.querySelectorAll('[name], [id], [for]').forEach(element => {
            ['name', 'id', 'for'].forEach(attr => {
                if (element.hasAttribute(attr)) {
                    let attrValue = element.getAttribute(attr);
                    attrValue = attrValue.replace(
                        new RegExp(`${this.prefix}-\\d+-`, 'g'),
                        `${this.prefix}-${newIndex}-`
                    );
                    element.setAttribute(attr, attrValue);
                }
            });
        });
        
        const hiddenId = newItem.querySelector(`input[name="${this.prefix}-${newIndex}-id"]`);
        if (hiddenId) hiddenId.value = '';
        
        // Asegurar que el checkbox active esté checked por defecto
        const activeCheckbox = newItem.querySelector(`input[name="${this.prefix}-${newIndex}-active"]`);
        if (activeCheckbox) activeCheckbox.checked = true;
        
        this.container.appendChild(newItem);
        this.totalFormsInput.value = currentTotal + 1;
    }

    createEmptyItem() {
        // Cambio: añadido campo active como checkbox hidden o visible
        const div = document.createElement('div');
        div.className = 'contact-item';
        div.innerHTML = `
            <input type="hidden" name="${this.prefix}-0-id" id="id_${this.prefix}-0-id">
            <input type="hidden" name="${this.prefix}-0-active" value="true" id="id_${this.prefix}-0-active">
            <label for="id_${this.prefix}-0-type">Type:</label>
            <select name="${this.prefix}-0-type" class="" id="id_${this.prefix}-0-type">
                <option value="phone" selected>📞</option>
                <option value="email">🖂</option>
                <option value="fax">🖷</option>
            </select>
            <span></span>
            <label for="id_${this.prefix}-0-value">Value:</label>
            <input type="text" name="${this.prefix}-0-value" class="" maxlength="50" id="id_${this.prefix}-0-value">
            <span></span>
            <label for="id_${this.prefix}-0-notes">Notes:</label>
            <input type="text" name="${this.prefix}-0-notes" class="" maxlength="50" id="id_${this.prefix}-0-notes">
            <span></span>
            <span></span>
            <button class="btn-delete-self" type="button"><i class="fi fi-sr-trash"></i></button>
        `;
        return div;
    }

    reindexAll() {
        const items = this.container.querySelectorAll(this.itemSelector);
        let newIndex = 0;
        
        items.forEach(item => {
            item.querySelectorAll('[name], [id], [for]').forEach(element => {
                ['name', 'id', 'for'].forEach(attr => {
                    if (element.hasAttribute(attr)) {
                        let attrValue = element.getAttribute(attr);
                        attrValue = attrValue.replace(
                            new RegExp(`${this.prefix}-\\d+-`, 'g'),
                            `${this.prefix}-${newIndex}-`
                        );
                        element.setAttribute(attr, attrValue);
                    }
                });
            });
            newIndex++;
        });
        
        this.totalFormsInput.value = newIndex;
    }
}

// Inicializar

let clientPane = document.querySelector('#client-pane');

const clientContactsFormset = new DynamicFormset({
    container: clientPane.querySelector('.contacts-container'),
    prefix: 'client_contacts',
    addButton: clientPane.querySelector('.btn-add-contact')
});

let claimPane = document.querySelector('#claim-pane');

const claimAdjusterContactsFormset = new DynamicFormset({
    container: claimPane.querySelector('.contacts-container'),
    prefix: 'claim_adjuster_contacts',
    addButton: claimPane.querySelector('.btn-add-contact')
});

let defPane = document.querySelector('#defense-pane');
console.log(defPane);

const defAttorneyContactsFormset = new DynamicFormset({
    container: defPane.querySelector('.contacts-container'),
    prefix: 'def_attorney_contacts',
    addButton: defPane.querySelector('.btn-add-contact')
});

console.log(defAttorneyContactsFormset);

const defAssistantContactsFormset = new DynamicFormset({
    container: defPane.querySelectorAll('.contacts-container')[1],
    prefix: 'def_assistant_contacts',
    addButton: defPane.querySelectorAll('.btn-add-contact')[1],
});