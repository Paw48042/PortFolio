export const getUserId = () => {
    return document.querySelector('#user_id').getAttribute('name');
}

export const getMissionRoom = () => {
    return document.querySelector('#roomname').getAttribute('name');
}

export const getMissionOwner = () => {
    return document.querySelector('#mission_owner').getAttribute('name');
}

// get Full name 

export const getFullName = () => {
    return document.querySelector('#user_id').dataset.fullName;
}