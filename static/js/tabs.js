

const form = document.querySelector('.form')
const tabBtns = document.querySelectorAll('.tab-btn');
const tabPanes = document.querySelectorAll('.tab-pane');
const prevBtn = document.getElementById('btn-prev');
const nextBtn = document.getElementById('btn-next');
const submitBtn = document.getElementById('btn-submit');
let currentTab = 1;

function activateTab(tabId) {
    currentTab = parseInt(tabId); 

    tabBtns.forEach(btn => {
        btn.classList.remove('active');
    })

    tabPanes.forEach(pane => {
        pane.classList.remove('active');
    });

    const activeBtn = Array.from(tabBtns).find(
        btn => btn.dataset.tab === tabId
    );
    
    const activePane = Array.from(tabPanes).find(
        pane => pane.dataset.tab === tabId
    ); 

    if (activeBtn)
        activeBtn.classList.add('active');

    if (activePane)
        activePane.classList.add('active');


    if (tabId === '1') {
        prevBtn.classList.remove('active');
    }
    else {
        prevBtn.classList.add('active');
    }

    if (tabId === ''+tabPanes.length) {
        nextBtn.classList.remove('active');
        submitBtn.classList.add('active');
    }
    else {
        nextBtn.classList.add('active');
        submitBtn.classList.remove('active');
    }
} 
tabBtns.forEach(btn => { 
    btn.addEventListener('click', function() {
        const tabId = this.dataset.tab;
        activateTab(tabId);
    })
});

nextBtn.addEventListener('click', function() {
    let activeIndex = currentTab;  
    let nextIndex = activeIndex + 1; 
    activateTab(''+nextIndex); 
});

prevBtn.addEventListener('click', function() {
    let activeIndex = currentTab;
    let prevIndex = activeIndex - 1; 
    activateTab(''+prevIndex);
});

