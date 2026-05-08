import { loadComponent } from "./load.js";

const addContactBtns = document.querySelectorAll('.btn-add-contact');
const btnAddInjury = document.querySelector('.btn-add-injury');
const btnDeleteSelves = document.querySelectorAll('.btn-delete-self');
const submitBtn = document.querySelector('#btn-submit'); 

addContactBtns.forEach(btn => {
    btn.addEventListener('click', async function() {
        let itemContainer = btn.parentElement.querySelector('.contact-item-container');            
        await loadComponent(itemContainer, 'contact-item.html');

        let contactItem = itemContainer.lastElementChild;
        let containerName = itemContainer.dataset.name; 

        contactItem.classList.add(containerName+'-contact-item')
        let contact_type = contactItem.querySelector('.select-contact-type');
        contact_type.name = containerName + '-contact-type'

        let contact_value = contactItem.querySelector('.input-contact-value');
        contact_value.name = containerName + "-contact-value";

        let contact_note = contactItem.querySelector('.input-contact-notes');
        contact_note.name = containerName + "-contact-notes"; 

        let deleteBtn = contactItem.querySelector('.btn-delete-self');
        deleteBtn.addEventListener('click', function() {
            deleteBtn.parentElement.remove();
        });
    })
});

btnAddInjury.addEventListener('click', function() {
    const itemContainer = btnAddInjury.parentElement.querySelector('.injury-item-container');
    const originalItem = itemContainer.firstElementChild;
    const injuryItem = originalItem.cloneNode(true);
    itemContainer.appendChild(injuryItem); 

    let idInput = injuryItem.querySelector('.input-injury-id');
    console.log(idInput);
    idInput.value="";


    let dateInput = injuryItem.querySelector('.input-injury-date');
    //dateInput.value = "";

    let selectPart = injuryItem.querySelector('.select-injury-body-part');
    selectPart.value = "";

    let selectType = injuryItem.querySelector('.select-injury-type');
    selectType.value = "";

    let btnDelete = injuryItem.querySelector('.btn-delete-self');

    btnDelete.addEventListener('click', function() {
        btnDelete.parentElement.remove();
    });
});

btnDeleteSelves.forEach(btn => {
    btn.addEventListener('click', function() {
        btn.parentElement.remove();
    });
});



let selects = [
    'client',
    'employer',
    'ins-carrier',
    'claim-admin',
    'claim-adj',
    'def-lawfirm',
    'def-att',
    'def-asst',
]

selects.forEach(id => {
    new TomSelect("#select-"+id, {
        create: true,
        sortField: {
            field: "text",
            direction: "asc"
        },
        onChange: function(value) {
            const hiddenName = document.querySelector('[name="'+id+'-name"]');
            console.log(hiddenName);

            if (!value) {
                hiddenName.value = "";
                return;
            }

            const option = this.options[value];


            if (option) { 
                hiddenName.value = ""; 
                console.log(document.querySelector('[name="'+id+'-id"]').value);
                
            } 
            else { 
                hiddenName.value = value;
                
                // limpiar el select para no enviar texto como id
                this.clear();
            }
        }
        
    });

});



