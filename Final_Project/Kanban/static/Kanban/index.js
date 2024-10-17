
// get csrf token
const csrftoken = getCookie('csrftoken');

document.addEventListener('DOMContentLoaded',function(){

    // add event listener to home link
    document.querySelector('#home').addEventListener('click',e => {
        e.preventDefault()
        // if click homepage , run this
        loadPage('index');
        load_default();
    })

    // add event listener to new task link 
    document.querySelector('#newTask').addEventListener('click', e => {
        e.preventDefault()
        // if click new task, run this code
        loadPage('new-task');
        get_user()
    })
    
    // add event listener to close btn in viewtask, edittask, createtask
    document.querySelectorAll('.btn-close').forEach(btn => {
        btn.addEventListener('click',()=> {
            loadPage('index');
            load_default();
        })
    })
    // add event listener to the create new task
    add_listener_to_create_task();

    // add event listener to edit task 
    add_listener_to_edit_task();

    // add event listener to delete task
    add_listener_to_delete_task();

    // add event listener to comment 
    add_listener_to_comment();
    
    
    // By default, load content after login 
     loadPage('index');
     load_default();

     window.onpopstate = function(event){
        loadPage(event.state.state);
    }
})




// load default page after login
function load_default(){
// remove all element first
document.querySelectorAll('.task-card-all').forEach((element)=>{
    element.remove();
})
    // fetch element 
    fetch('/api/get_task')
    .then(response => response.json())
    .then(data => {
        
        data.forEach(items => {        
            // for each data, create div element
            const element = document.createElement('div');
            element.classList.add('card','p-2','m-1','mb-3','task-card-all','animate__animated','animate__faster','transparent_card');
            element.setAttribute('id',`task-${items.id}`);
            element.dataset.owner = items.createBy.id;           
            element.innerHTML = `
                <div class="card-body">
                    <p style = "font-size : 12px;"><img class = "profilepic" src = ${items.createBy.profilePic} alt = "Image"> ${items.createBy.username}</p>
                    <p style = "font-size : 12px;">${items.taskName}</p>
                </div>`;

            const user = document.querySelector('#userID_ishere');
            // if user are an owner of the task or an admin give them a button 
            if ((element.dataset.owner === user.getAttribute('name') ) || user.dataset.role === 'A'){
                const button = createButton(items.id)
                button.addEventListener('click', event => {
                    if(event.target === document.querySelector(`#button-${items.id}`)){
                        makeProgress(element,items.id,items.status);     
                    }
                        
                    })
                element.append(button)
            }
            // add event listener, so when click at the task, can go and see all the detail 
            element.addEventListener('click',(event)=>{
                if (event.target !== document.querySelector(`#button-${items.id}`)){
                    loadPage('view-task');
                    view_task_detail(items.id);
                    // get the comment
                    get_comment(items.id);
                }
            })
            // let's card fall in line
            fallIn(element,items.status, items.id)
            
        });
    })
    .catch(error => {
        console.log('Error during fetch' + error)
    });

}

function createButton(id){
    const button = document.createElement('button');
            button.classList.add('button-48','transparent_card');
            button.setAttribute('id', `button-${id}`);
            button.setAttribute('role','button');
            button.innerHTML = '<span class="material-icons">done</span>'
    return button
}

// To choose which line to go in
function fallIn(element, status, taskID){

    // if task = TODO, let the card fall in TODO LIST
   if (status === "T"){      
        document.querySelector('#TODOLIST').append(element);
    }
    // if the card = Process, let the card fall in process list
    else if (status === "P"){
        // attach element in process

            document.querySelector("#PROCESSLIST").append(element);
        
        
        const user = document.querySelector('#userID_ishere');
        // after that, add one
        if (element.dataset.owner == user.getAttribute('name') || user.dataset.role == 'A'){
            try{
                document.querySelector(`#button-${taskID}`).remove()
            }
            catch(error){
                console.log('Error at fall in : ' + error);
            }
            const button = createButton(taskID)
            button.addEventListener('click', event => {
                if(event.target === document.querySelector(`#button-${taskID}`)){
                    makeProgress(element,taskID,status);   
                }
            })
            element.append(button)
        }
        

    }
    else if (status === "F"){
        // attach element in Finish
        document.querySelector("#FINISHLIST").append(element)

        // there's a button, so remove. We don't want a button here 
        try{
            document.querySelector(`#button-${taskID}`).remove()
        }
        catch(error){
            console.log('error at fall in (F) : ' + error)
        }
        
    }
    else{
        console.log("Error, There is no such status")
    }


}

// To update each task card
function makeProgress(element,taskID,status){


    if (status === "T"){
        status = "P"
    }
    else if (status === "P"){
        status = "F"
    } 
    
    return fetch(`/api/make_progress/${taskID}`,{
        method : 'PUT',
        headers: {
            'Content-Type': 'application/json', 
            'X-CSRFToken': csrftoken,
        },
        body : JSON.stringify({
            "status" : status,
        })
    })
    .then(response => response.json())
    .then(data => {
            const substitute = element 
            //remove the element
            element.classList.add('animate__flipOutX');
            setTimeout(()=>{
                element.classList.remove('animate__flipOutX');
                element.remove()
                fallIn(substitute, status, taskID);
                element.classList.add('animate__flipInX'); 
            },500)
            
            setTimeout(element.classList.remove('animate__flipInX'),500)
            
        })
            
            
        
}


/* BELOW IS FUNCTION THAT's LOOK FINE. SADLY, ABOVE IS NOT */

function view_task_detail(taskID){

    return fetch(`/api/get_one_task/${taskID}`)
           .then(response => response.json())
           .then(data => {
            // implement logic here

            // change the header
            const taskHeader = document.querySelector('#task-header');
            taskHeader.innerHTML = data.taskName;
            taskHeader.setAttribute('name',data.id)
        
            // if there is an element before, remove it first
            // remove button first
            try{
                document.querySelector('#edit-button').remove();
            }
            catch(error){
                console.log('No edit btn to remove : '+error)
            }
            try{
                document.querySelector('#taskContent').remove(); 
            }
            catch(error){
                console.log('No task content to remove :' + error )
            }
            
            // if user create this task
            if (data.createBy.id === Number(document.querySelector('#userID_ishere').getAttribute('name')) || document.querySelector('#userID_ishere').dataset.role === 'A'){

                const editBtn = document.createElement('a')
                editBtn.classList.add('text-end', 'px-2', 'mx-2');
                editBtn.setAttribute('id', 'edit-button');
                editBtn.setAttribute('href', '#');
                editBtn.innerHTML = "Edit Task";

                editBtn.addEventListener('click', event => {
                    event.preventDefault()
                    loadPage('edit-task');
                    // add data to a form and then submit
                    editForm(data)
                })
                // append button
            document.querySelector('#to-add-edit-button').append(editBtn);

            }
        
            // get the assigned person
            let content = ''
            for( let i = 0; i < data.assigned.length; i++){
                content += `<li> <img class = "profilepic" src = ${data.assigned[i].profilePic} alt = "Image"> ${data.assigned[i].username}</li>`
            }
            // create element 
            const element = document.createElement('div');
            element.setAttribute('id','taskContent')
            element.innerHTML = `
                                    <div class = "row text-start">
                                        <p>Owner: ${data.createBy.username}</p>
                                        <p>Created: ${handleDate(data.createTime)}</p>
                                        <p> Status : ${checkStatus(data.status)}</p>
                                    </div>
                                    <div class = "m-3 pb-3">
                                    <h6>Description</h6>
                                    <hr>
                                    <p>${data.detail}</p>
                                    </div>
                                    <div class = "m-3">
                                        <h6>Assigned to</h6>
                                        <hr>
                                        <ul>${content}</ul>
                                    </div>
                                    
                                    `
            
            document.querySelector('#single-card-task').append(element);
        })
}

function editForm(data){

    // add value into an edit form 
    document.querySelector('#taskID_ishere').setAttribute('name',data.id)
    const taskName = document.querySelector('#edit-task-name'); // task Name
    const taskDetail = document.querySelector('#edit-task-detail'); // task Detail 
    taskName.value = data.taskName;
    taskDetail.value = data.detail;
    
    document.querySelectorAll('.editcheck').forEach(element =>{
        element.remove();

       });

    // check box for every employee in company
     get_user('edit')
     .then(()=> {
        data.assigned.forEach(person => {
        document.querySelector(`#edit${person.username}`).checked = true;})
    })

    // for the progress form
    if (data.status === 'T'){
        document.querySelector('#inlineRadio1').checked = true;
    }
    else if(data.status === 'P'){
        document.querySelector('#inlineRadio2').checked = true;
    }
    else if(data.status === 'F'){
        document.querySelector('#inlineRadio3').checked = true;
    }
}

function get_user(str_edit = ""){ // take string parameter "edit" or ""
    return fetch('/api/get_user')
           .then(response => response.json())
           .then(data => {
            // create array to get the element 
            const elementList = []
            data.forEach(person => {

                // create a div
                if (!document.querySelector(`#${str_edit}${person.username}`)){
                    const element = document.createElement('div')
                    element.classList.add('form-check','form-check-inline','editcheck')
                    element.innerHTML = `<input class="form-check-input" type="checkbox" name = "assignedID" value="${person.id}" id="${str_edit}${person.username}">
                                        <label class="form-check-label" for="${str_edit}${person.username}">
                                        <img class = "profilepic" src = ${person.profilePic} alt = "Image">
                                        ${person.username} : ${person.first_name} ${person.last_name}
                                        </label>`;
                                        
                    element.checked = false;
                    elementList.push(element)
                }
            }
                
            )
                return elementList
           })
           .then(elementList => {
            elementList.forEach(items =>{
                // if no items
                if (!document.querySelector(`#${str_edit}${items.username}`)){
                      // append element to the list                      
                      document.querySelector(`#${str_edit}employee`).append(items);    
                }
           });
        })
}

function create_task(taskName, detail, assigned){

    // userid
    const userID = document.querySelector('#userID_ishere').getAttribute('name')

    return fetch('/api/create_task',{
        method : "POST",
        headers: {
            'Content-Type': 'application/json', 
            'X-CSRFToken': csrftoken,
        },
        body : JSON.stringify({
            "taskName" : taskName,
            "detail": detail,
            "createBy" : userID,
            "assigned" : assigned,
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
    })
    .catch(error => {
        console.log(error)
    })
}

// to get csrf token
// from django official website
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// Just to handle date to be human-readable format
function handleDate(date){
    const dt = new Date(date)

    return dt.toLocaleString()

}

// Use to choose which page gonna pop up and which page gonna be disappear
function loadPage(page){
    // show page
    if (page === "index"){
       document.querySelector('#index').style.display = '';
       document.querySelector('#new-task').style.display = 'none';
       document.querySelector('#edit-task').style.display = 'none';
       document.querySelector('#view-task').style.display = 'none';
       history.pushState({state: 'index'},"",'/');

    } 
    else if (page === "new-task"){

       // show new task page 
       document.querySelector('#index').style.display = 'none';
       document.querySelector('#new-task').style.display = '';
       document.querySelector('#edit-task').style.display = 'none';
       document.querySelector('#view-task').style.display = 'none';
       history.pushState({state: 'new-task'},"",'/create-new-task');
    }
    else if (page === 'edit-task'){
       document.querySelector('#index').style.display = 'none';
       document.querySelector('#new-task').style.display = 'none';
       document.querySelector('#edit-task').style.display = '';
       document.querySelector('#view-task').style.display = 'none'
       history.pushState({state: 'edit-task'},"",'/edit-task');
    }
    else if(page === 'view-task'){
        document.querySelector('#index').style.display = 'none';
        document.querySelector('#new-task').style.display = 'none';
        document.querySelector('#edit-task').style.display = 'none';
        document.querySelector('#view-task').style.display = '';
        history.pushState({state: 'view-task'},"",'/view-task-detail');

    }
}
// to return full status name
function checkStatus(status){
    if (status === "T"){
        return "Todo"
    }
    else if (status === "P"){
        return "Procesing"
    }
    else if( status === "F"){
        return "Finish"
    }
    else{
        return "404 status not found"
    }
}

function edit_task(taskID, taskName, taskDetail, assigned, status){

    if (assigned.length === 0){
        console.log('stop user from submitting')
        return false
    }

    
    return fetch(`/api/edit_task/${taskID}`,{
        method : 'PUT',
        headers: {
            'Content-Type': 'application/json', 
            'X-CSRFToken': csrftoken,
        },
        body : JSON.stringify({
            taskName : taskName,
            detail : taskDetail,
            assigned : assigned,
            status : status
        })
    })
    .then(response => response.json())
}

function delete_task(taskID){
    return fetch(`/api/delete_task/${taskID}`,{
        method : 'DELETE',
        headers: {
            'Content-Type': 'application/json', 
            'X-CSRFToken': csrftoken,
        },
        body : JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
    })
    .catch(error => {
        console.log(error)
    })
}

function add_listener_to_create_task(){
    document.querySelector('#submit-task').addEventListener('click',(event)=> {
        // stop the form from submitting
        event.preventDefault()

        // check if event listener added

        const form = document.querySelector('#task-form');
        const submitter = document.querySelector('#submit-task');
        const formData = new FormData(form, submitter)

        // see if value is arrive
        const task = formData.get('taskName');
        const detail = formData.get('taskDetail');
        const assigned = formData.getAll('assignedID');
        
        // when click, send data from a form to server
        create_task(task, detail, assigned)
        .then(() => {
            document.querySelector('#task-form').reset();
            loadPage('index');
            load_default();
        })
    })  

}

function add_listener_to_comment(){
    // select comment btn
    document.querySelector('#make-comment').addEventListener('click',event => {
        // stop from submitting
        event.preventDefault()

        // get taskID 
        const taskID = document.querySelector('#task-header').getAttribute('name');

        // create form data 
        const commentForm = document.querySelector('#comment-form')
        const submitter = document.querySelector('#make-comment')
        const commentFormData = new FormData(commentForm,submitter) 
        // get comment value 
        const commentDetail = commentFormData.get('comment')

        post_comment(taskID,commentDetail)
        .then(() => {
            document.querySelector('#comment-form').reset();
            get_comment(taskID)
            loadPage('view-task');
        })

    })
}

function add_listener_to_edit_task(){
    document.querySelector('#edit-submit-task').addEventListener('click', (event)=>{
        // stop from submitting a form
        event.preventDefault();

        // get taskID 
        const taskID = document.querySelector('#taskID_ishere').getAttribute('name')
        // create form data
        const editForm2 = document.querySelector('#edit-task-form')
        const submitter = document.querySelector('#edit-submit-task')
        const editFormData = new FormData(editForm2, submitter)

        const taskName = editFormData.get('taskName');
        const taskDetail = editFormData.get('taskDetail');
        const assigned = editFormData.getAll('assignedID');
        const status = editFormData.get('task-status-check')

        edit_task(taskID, taskName, taskDetail, assigned, status)
        .then(e => {
            loadPage('index');
            load_default();
        })

    })
}

function add_listener_to_delete_task(){
    document.querySelector('#delete-task').addEventListener('click', (event)=>{
        // stop from submitting     
        event.preventDefault();
        // task ID
        let taskID = document.querySelector('#taskID_ishere').getAttribute('name')

        delete_task(taskID)
        .then(() => {
            loadPage('index');
            load_default();
        })
    })
}

async function get_comment(taskID){

    try{

        // remove existing element first
        document.querySelectorAll('.to-remove-comment').forEach(element =>{
            element.remove()
        })

        const response  = await fetch(`api/get_comment/${taskID}`)
        const data = await response.json();

        // implement logic here 

        data.forEach(async comment => {
            // create comment
            const element = document.createElement('div');
            element.classList.add('card','to-remove-comment', 'm-3', 'transparent_card')
            element.setAttribute('id',`comment-${comment.id}`)
            element.innerHTML = `<div class="card-body transparent_card">
                                    <img class = "profilepic" src = ${comment.author.profilePic }>
                                    <b>${comment.author.username} </b>
                                    <hr>
                                    <p>${comment.comment}</p>
                                </div>`
            document.querySelector('#append-comment-here').append(element);
            
        })
    }
    catch(error){
        console.log(error)
    }
}

async function post_comment(taskID,comment){
    // userid
    const userID = document.querySelector('#userID_ishere').getAttribute('name'); 

    try{
        const response = await fetch(`/api/post_comment/${taskID}`,{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                "author" : userID,
                "taskToComment" : taskID,
                "comment" : comment,
            })
        })
        const data = await response.json()
        console.log(data)
        return data
    }
    catch(error){
        console.log('fail to post comment, Error : ' + error);
    }

}