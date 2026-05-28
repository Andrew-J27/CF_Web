import {show, hide, isActive} from './base.js';

const fade = document.querySelector('.modal.fade');

/* Tomar datos de la fila y llenar el form */
function fillUpdateForm(btn, form) { 
    const row = btn.closest('tr');
    const cells = row.querySelectorAll('td');

    cells.forEach(cell => { 
        const field = cell.dataset.field;
        const input = form.querySelector(`[name="${field}"]`);  
        if (input) {
            if (input && input.type === 'date') {
                
                input.value = cell.dataset.date; 
            } 
            else input.value = cell.textContent;  
        }
    }); 
}

const clearSearch = document.querySelector('.btn-clear');

if (clearSearch) {
    clearSearch.addEventListener('click', function() { 
        const input = clearSearch.parentElement.querySelector('.search');
        input.value = "";
        clearSearch.closest('form').submit();
    });
}

// En tu template o archivo .js
document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar todas las filas que tienen data-url
    const rows = document.querySelectorAll('tr[data-url]');
    
    rows.forEach(row => {
        row.addEventListener('dblclick', function() {
            const url = this.getAttribute('data-url');
            if (url) {
                window.location.href = url;
            }
        });
        
        // Opcional: cambiar el cursor para indicar que es clickeable
        row.style.cursor = 'pointer';
    });
});

const search_form = document.querySelector('form.search'); 
const filters = search_form.querySelectorAll('select');

filters.forEach(filter => {
    filter.addEventListener('change', function() {
        search_form.submit();
    });
});

/* Interacciones de botones de CRUD,
   fila de la tabla y formulario  */
function crudActions(btns, modal, form) {

    btns.forEach(btn => {
        btn.addEventListener('click', function() {
            const id = btn.dataset.id;

            if (id) {
                const title = form.querySelector('.title-name'); 
                title.textContent = '"'+btn.dataset.name+'';
    
                const url = form.dataset.url;
                let action = url.replace(/\/(\d+)\//, `/${id}/`);
                form.action = action;
                fillUpdateForm(btn, form);
            } 
            
            if (!(document.querySelector('.model-name').textContent === "Case Registers"  // Excepcion de create/update case
            && (btn.classList.contains('btn-update') || btn.classList.contains('btn-create')))) {

                show(fade);
                show(modal);
                console.log(document.querySelector('.model-name').textContent)
            }
            
        });
    });
}




const deleteBtns = document.querySelectorAll('.btn-delete'); 
const deleteModal = document.querySelector('.modal-delete');
const deleteForm = document.querySelector('.delete-form');

crudActions(deleteBtns, deleteModal, deleteForm);

const restoreBtns = document.querySelectorAll('.btn-restore'); 
const restoreModal = document.querySelector('.modal-restore');
const restoreForm = document.querySelector('.restore-form');

crudActions(restoreBtns, restoreModal, restoreForm);

/* */
const createBtn = document.querySelectorAll('.btn-create');
const createModal = document.querySelector('.modal-create');
const createForm = document.querySelector('.create-form');

crudActions(createBtn, createModal, createForm);

const updateBtns = document.querySelectorAll('.btn-update'); 
const updateModal = document.querySelector('.modal-update');
const updateForm = document.querySelector('.update-form');

crudActions(updateBtns, updateModal, updateForm);

if (isActive(createForm) || isActive(updateForm) ||
    isActive(deleteForm) || isActive(restoreForm)) {

        show(fade);
    }

const closeModalBtns = document.querySelectorAll('.btn-close-modal');

closeModalBtns.forEach(btn => {
    btn.addEventListener('click', function() {
        hide(btn.closest('.modal'));
        hide(fade);
    });
});


