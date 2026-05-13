class DynamicInjuryFormset {
    constructor(options) {
        this.container = options.container;
        this.prefix = options.prefix;
        this.addButton = options.addButton;
        
        this.totalFormsInput = this.container.querySelector(`input[name="${this.prefix}-TOTAL_FORMS"]`);
        this.itemSelector = '.injury-item';
        this.deleteSelfBtnSelector = '.btn-delete-self';
        // Usamos active checkbox para soft delete
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

    // Método para soft delete
    handleSoftDelete(button) {
        const injuryItem = button.closest(this.itemSelector);
        if (!injuryItem) return;

        const hiddenId = injuryItem.querySelector(`input[name^="${this.prefix}-"][name$="-id"]`);
        const isExisting = hiddenId && hiddenId.value !== '';
        
        if (!isExisting) {
            // Elemento nuevo - eliminar del DOM
            const minForms = parseInt(this.container.querySelector(`input[name="${this.prefix}-MIN_NUM_FORMS"]`).value);
            const currentItems = this.container.querySelectorAll(this.itemSelector);

            if (currentItems.length <= minForms) { 
                return;
            }
            injuryItem.remove();
            this.reindexAll();
        } else {
            // Elemento existente - toggle del estado active
            const activeCheckbox = injuryItem.querySelector(this.activeCheckboxSelector);
            if (activeCheckbox) {
                const isCurrentlyInactive = injuryItem.classList.contains('inactive');
                
                if (!isCurrentlyInactive) {
                    // Marcar como inactivo (soft delete)
                    injuryItem.classList.add('inactive');
                    activeCheckbox.checked = false; // false = inactivo
                    
                    // Desactivar campos visualmente
                    injuryItem.querySelectorAll('input, select, textarea, button').forEach(field => {
                        if (!field.matches(this.deleteSelfBtnSelector)) {
                            field.disabled = true;
                            field.readOnly = true;
                        }
                    });
                    
                    // Opcional: agregar estilo visual
                    injuryItem.style.opacity = '0.6';
                } else {
                    // Reactivar elemento
                    injuryItem.classList.remove('inactive');
                    activeCheckbox.checked = true; // true = activo
                    
                    // Reactivar campos
                    injuryItem.querySelectorAll('input, select, textarea, button').forEach(field => {
                        field.disabled = false;
                        field.readOnly = false;
                    });
                    
                    // Restaurar estilo
                    injuryItem.style.opacity = '1';
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
                } else if (input.type === 'date') {
                    input.value = '';
                } else {
                    input.value = '';
                }
            });
            
            // Limpiar selects (resetear a primera opción)
            newItem.querySelectorAll('select').forEach(select => {
                select.selectedIndex = 0;
            });
            
            // Limpiar textareas
            newItem.querySelectorAll('textarea').forEach(textarea => {
                textarea.value = '';
            });
        }
        
        // Asegurar que no tenga clase inactive
        newItem.classList.remove('inactive');
        newItem.style.opacity = '1';
        
        newItem.querySelectorAll('input, select, textarea, button').forEach(field => {
            field.disabled = false;
            field.readOnly = false;
        });
        
        const newIndex = currentTotal;
        
        // Reemplazar índices en name, id, for
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
        
        // Limpiar el hidden id
        const hiddenId = newItem.querySelector(`input[name="${this.prefix}-${newIndex}-id"]`);
        if (hiddenId) hiddenId.value = '';
        
        // Asegurar que el checkbox active esté checked por defecto
        const activeCheckbox = newItem.querySelector(`input[name="${this.prefix}-${newIndex}-active"]`);
        if (activeCheckbox) activeCheckbox.checked = true;
        
        this.container.appendChild(newItem);
        this.totalFormsInput.value = currentTotal + 1;
    }

    createEmptyItem() {
        const div = document.createElement('div');
        div.className = 'injury-item';
        div.innerHTML = `
            <input type="hidden" name="${this.prefix}-0-id" id="id_${this.prefix}-0-id">
            <input type="hidden" name="${this.prefix}-0-active" value="true" id="id_${this.prefix}-0-active">
            
            <label for="id_${this.prefix}-0-date">Date:</label>
            <input type="date" name="${this.prefix}-0-date" class="form-field" id="id_${this.prefix}-0-date">
            
            <label for="id_${this.prefix}-0-part">Body Part:</label>
            <select name="${this.prefix}-0-part" class="form-field" id="id_${this.prefix}-0-part">
                <option value="">---------</option>
                <!-- Las opciones se cargarán desde el backend -->
            </select>
            
            <label for="id_${this.prefix}-0-type">Injury Type:</label>
            <select name="${this.prefix}-0-type" class="form-field" id="id_${this.prefix}-0-type">
                <option value="">---------</option>
                <!-- Las opciones se cargarán desde el backend -->
            </select>
            
            <button class="btn-delete-self" type="button"><i class="fi fi-sr-trash"></i> Remove</button>
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

// Para el formset de injuries
let casePane = document.querySelector('#injury-pane'); // o el contenedor apropiado

const injuryFormset = new DynamicInjuryFormset({
    container: casePane.querySelector('.injuries-container'),
    prefix: 'injuries',  // Asegúrate que coincida con el prefix de tu formset
    addButton: casePane.querySelector('.btn-add-injury')
});