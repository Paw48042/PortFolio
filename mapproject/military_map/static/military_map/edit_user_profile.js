

document.addEventListener('DOMContentLoaded', e => {

    // If click at the edit btn, the bootstrap effect changes from prohibit to editable 
    
    // click button and 
    const editBtn = document.querySelector("#makeChange");

    editBtn.addEventListener('click', e => {
        if (editBtn.textContent === "Edit"){
            // remove the fieldset 
            editBtn.remove();
            document.querySelector('#Update').style.display = 'block';
            document.querySelector('#customFieldset').removeAttribute('disabled');
        }
    })


})
