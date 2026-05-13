const createBtn = document.querySelector('.btn-create');
const updateBtns = document.querySelectorAll('.btn-update');
const createUrl = document.querySelector('.create-form').action;
const updateUrl = document.querySelector('.update-form').dataset.url;

console.log(createUrl);

createBtn.addEventListener('click', function() { 
    const redirectUrl = createUrl;
    window.location.href = redirectUrl;
    console.log(redirectUrl);
});

updateBtns.forEach(btn => {
    btn.addEventListener('click', function() {
        const id = btn.dataset.id;
        const redirectUrl = updateUrl.replace(/\/(\d+)\//, `/${id}/`);
        window.location.href = redirectUrl;
        console.log(redirectUrl);
    })
});