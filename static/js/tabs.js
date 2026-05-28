const tabs = document.querySelector('.tabs');
const tab_btns = tabs.querySelectorAll('.tab-btn');
const tab_panes = tabs.querySelectorAll('.tab-pane');
const next_btn = tabs.querySelector('.btn-next');
const prev_btn = tabs.querySelector('.btn-prev');
const submit_btn = tabs.querySelector('.btn-submit');

if (tabs.dataset.create === "1") {
    tabs.querySelector('button[data-tab="6"]').style.display = 'none';
    tabs.querySelector('button[data-tab="7"]').style.display = 'none';
    tabs.querySelector('div[data-tab="6"]').style.display = 'none';
    tabs.querySelector('div[data-tab="7"]').style.display = 'none';
    
    tabs.dataset.max = "5"
}

let currentTabId = "1";
let maxTab = tabs.dataset.max; 

function isLastTabActive() {
    if (currentTabId === maxTab) 
        return true;
    else
        return false;
}

function isFirstTabActive() {
    if (currentTabId === "1") 
        return true;
    else
        return false;
}

function manageControls() { 

    if (isFirstTabActive())
        prev_btn.classList.remove('active');
    else
        prev_btn.classList.add('active');

    if (isLastTabActive()) 
        next_btn.classList.remove('active');
    else
        next_btn.classList.add('active');

    // Submit Button
    if (isLastTabActive()) 
        submit_btn.classList.add('active'); 
    else 
        submit_btn.classList.remove('active');
}

function activateTab(tabId) {

    let activeTab = tabs.querySelector('.tab-btn.active');
    let activePane = tabs.querySelector('.tab-pane.active');

    activeTab.classList.remove('active');
    activePane.classList.remove('active');

    currentTabId = tabId;

    activeTab = tabs.querySelector('.tab-btn[data-tab="'+tabId+'"]');
    activePane = tabs.querySelector('.tab-pane[data-tab="'+tabId+'"]');

    activeTab.classList.add('active');
    activePane.classList.add('active');

    manageControls();
}


const initial = tabs.dataset.initial;

activateTab(initial);



tab_btns.forEach(btn => {
    btn.addEventListener('click', function() { 
        activateTab(btn.dataset.tab);
    });
});

next_btn.addEventListener('click', function() { 
    if (!isLastTabActive())
        activateTab(String( parseInt(currentTabId)+1));
});

prev_btn.addEventListener('click', function() { 
    if (!isFirstTabActive())
        activateTab(String( parseInt(currentTabId)-1));
});

const form = document.querySelector('.form');

submit_btn.addEventListener('click', function() {
    form.submit();
});
 