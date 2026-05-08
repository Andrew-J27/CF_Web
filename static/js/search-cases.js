document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('.table-row').forEach(row => {
        row.addEventListener('dblclick', function() {
            const url = this.getAttribute('data-url');
            window.location.href = url;
        });
    });

    btnDeleteSearch = document.querySelector('.btn-delete-search');
    searchInput = document.querySelector('.input-search');
    filterSelect = document.querySelector('.select-filter');
    form = document.querySelector('.search'); 

    btnDeleteSearch.addEventListener('click', function() {
        searchInput.value = ""; 
        filterSelect.value = "";
        form.submit();
    });

    filterSelect.addEventListener('change', () => {
        form.submit();
    });

    
});
