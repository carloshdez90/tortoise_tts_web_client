document.addEventListener('submit', (e) => {
    var button = document.getElementById('submit')
    var loader = document.getElementsByClassName('loader')[0]


    button.disabled = true
    loader.style.display = 'initial'
});