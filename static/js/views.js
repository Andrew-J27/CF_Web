document.addEventListener('DOMContentLoaded', function() {

    const rows = document.querySelectorAll('.table-row');
    const btnAdd = document.querySelector('.btn-add'); 
    const form = document.querySelector('.item-form');  
    const closeForm = form.querySelector('.btn-close'); 

    const name = document.querySelector('.view-container').dataset.name;

    const formTitle = form.querySelector('h2');

    const inputs = form.querySelectorAll('input');

    btnCreate = document.querySelector('.btn-create');
    btnDelete = document.querySelector('.btn-delete');
    btnSave = document.querySelector('.btn-save');
    
    // let closeEditForm = editForm.querySelector('.btn-close');

    function clearForm() {
        inputs.forEach(input => {
            if (input.name != "csrfmiddlewaretoken") input.value="";
        });
    }

    function clearRows() {
        rows.forEach(row => {
            row.classList.remove('selected');
        })
    }

    btnAdd.addEventListener('click', function() {
        formTitle.textContent = "New "+name;
        clearRows();
        clearForm();
        
        btnDelete.classList.remove('active');
        btnDelete.disabled = true;
        btnSave.classList.remove('active');
        btnSave.disabled = true;
        btnCreate.classList.add('active');
        btnCreate.disabled = false;

        form.classList.add('active');
    });

    closeForm.addEventListener('click', function() {
        clearRows();
        clearForm();
        form.classList.toggle('active');
    });

    rows.forEach(row => {
        row.addEventListener('dblclick', function() { 
            clearRows();
            row.classList.add('selected');
            formTitle.textContent = "Edit "+name;
            form.classList.add('active');

            btnDelete.classList.add('active');
            btnDelete.disabled = false;
            btnSave.classList.add('active');
            btnSave.disabled = false;
            btnCreate.classList.remove('active');
            btnCreate.disabled = true;

            row.querySelectorAll('td').forEach(td => {
                const field = td.dataset.field;
                const input = document.querySelector(`[name="${field}"]`);
                if (input.type === 'date') td.textContent = td.textContent.trim();
                if (input) input.value = td.textContent;
    
            }); 
            /*
            */
        });
    });  

    
});