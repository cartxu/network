document.addEventListener('DOMContentLoaded', function() {

    const edit = document.querySelectorAll('.editar');
    const like = document.querySelectorAll('.like');
    const del = document.querySelectorAll('.delete');
    const unlike = document.querySelectorAll('.unlike');

    edit.forEach(element => {
        element.addEventListener('click', () => {
            edit_view(element);
        });
    });

    unlike.forEach(element => {
        element.addEventListener('click', () => {
            unlike_post(element);
        })
    })

    like.forEach(element => {
        element.addEventListener('click', () => {
            like_post(element);
        });
    })

    del.forEach(element => {
        element.addEventListener('click', () => {
            delete_post(element);
        })
    })
    

});

function mensaje_alerta(){
    const mensaje = document.querySelector('#mensaje');
    mensaje.style.display = 'none';
    
}

function delete_post(element) {
    const id = element.getAttribute("data-id");
    const postBody = document.querySelector(`#postbody-${id}`);
    const img = document.querySelector(`#img-${id}`);
    let mensaje = document.querySelector('#mensaje');
    
    const form = new FormData();
    form.append("id", id);
    let alerta = confirm("Do you really want to delete this post?");
   
    if (alerta==true) {
        
        fetch("/delete/", {
            method: "POST",
            body: form,
        })
        .then(res => {
            if(img){
                img.style.display = 'none';
            }
            postBody.style.display = 'none';
            mensaje.style.display = 'block';
            mensaje.innerHTML = '<div class="alert alert-danger" role="alert"> You post has been deleted!</div>';
            setTimeout('mensaje_alerta()',3000);
        })

        
    } 
    

    
}

function unlike_post(element) {
    const id = element.getAttribute("data-id");
    const unlikeBtn = document.querySelector(`#unlikePost-${id}`);

    const form = new FormData();
    form.append("id", id);
    
    fetch("/like/", {
        method: "POST",
        body: form,
    })
    .then(res => res.json())
    .then(res => {
        document.querySelector(`#postLikes-${id}`).textContent = res.count;
        unlikeBtn.classList.toggle("fas");
        
    });

}


function like_post(element) {
    const id = element.getAttribute("data-id");
    const likeBtn = document.querySelector(`#likePost-${id}`);


    const form = new FormData();
    form.append("id", id);
    
    fetch("/like/", {
        method: "POST",
        body: form,
    })
    .then(res => res.json())
    .then(res => {
        document.querySelector(`#postLikes-${id}`).textContent = res.count;
        likeBtn.classList.toggle('fas');
        
    });
}


function edit_post(id, post){
    const newPost = new FormData()
    newPost.append("id", id);
    newPost.append("post", post);

    fetch("/edit/", {
        method: "POST",
        body: newPost,
    })
    .then((res) => {
        document.querySelector(`#postView-${id}`).textContent = post;
        document.querySelector(`#postView-${id}`).style.display = "block";
        document.querySelector(`#editView-${id}`).style.display = "none";
        document.querySelector(`#editView-${id}`).value = post;
    });
}


function edit_view(element) {

    let id = element.getAttribute("data-id"); //obtenemos el id del elemento seleccionado
    const editView = document.querySelector(`#editView-${id}`); 
    const postView = document.querySelector(`#postView-${id}`);

    editView.style.display = 'block'; //mostramos la vista de edición
    postView.style.display = 'none'; //escondemos el post 

    const cancelBtn = document.querySelector(`#cancel-${id}`);

    cancelBtn.addEventListener('click', () => { //añadimos eventlistener al boton cancelar 
        editView.style.display = 'none'; //ocultamos la vista de edición
        postView.style.display = 'block';
    });

    const saveBtn = document.querySelector(`#postSave-${id}`);

    saveBtn.addEventListener('click', () => {
        edit_post(id, document.querySelector(`#textArea-${id}`).value);
    });


}
