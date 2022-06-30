let todos_count = document.getElementsByClassName('todo').length
let complete_btns = document.getElementsByClassName('complete')
let edit_btns = document.getElementsByClassName('edit')
let delete_btns = document.getElementsByClassName('delete')

for(let i=0;i<todos_count;i++){  
    complete_btns[i].addEventListener('click', function(){
        let todo_id = this.dataset.id
        complete_todo(todo_id)
    })
    
    edit_btns[i].addEventListener('click', function(){
        let todo_id = this.dataset.id
        let url = `/edit/${todo_id}`
        window.location.href = url
    })
    delete_btns[i].addEventListener('click', function(){
        let todo_id = this.dataset.id
        trash_todo(todo_id)
    })
}


function complete_todo(id){
    fetch('/complete_todo/', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'id':id}) 
    })
    .then((response) => {
        if(response.ok){
            removeTodo(id)
        }
    })
}


function trash_todo(id){
    fetch('/trash_todo/', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'id':id}) 
    })
    .then((response) => {
        if(response.ok){
            removeTodo(id)
        } else {
            console.log('error')
        }
    })
}


function removeTodo(id){
    let todo_id = `todo-${id}`
    let todo = document.getElementById(todo_id)
    todo.remove()
    let todo_num_elem = document.getElementById('todo_nums')
    todos_count -= 1
    todo_num_elem.innerText = todos_count
    if(todos_count<=0){
        let active_info_elem = document.getElementById("active-info")
        let todo_container = document.getElementById("todo-container")
        let no_todos_elem = document.getElementById("no-todos")
        active_info_elem.classList.add("hidden")
        todo_container.classList.add("hidden")
        no_todos_elem.classList.remove("hidden")
    }
}
