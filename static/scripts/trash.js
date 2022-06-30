let todos_count = document.getElementsByClassName('todo').length
let restore_btns = document.getElementsByClassName('restore')
let delete_btns = document.getElementsByClassName('delete')

for(let i=0;i<todos_count;i++){
    restore_btns[i].addEventListener('click', function(){
        let todo_id = this.dataset.id
        restore_todo(todo_id)
    })
    delete_btns[i].addEventListener('click', function(){
        let todo_id = this.dataset.id
        if(confirm("confirm deletion?")==true){
            delete_todo(todo_id)
        }
    })
}


function restore_todo(id){
    fetch('/untrash_todo/', {
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

function delete_todo(id){
    fetch('/delete_todo/', {
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
            console.log('todo deleted!')
        } else {
            console.log('error')
        }
    })
}



function removeTodo(id){
    let todo_id = `todo-${id}`
    let todo = document.getElementById(todo_id)
    todos_count -= 1
    todo.remove()
    if(todos_count<=0){
        let title_container = document.getElementById("trash-title")
        let todo_container = document.getElementById("todo-container")
        let no_todos_elem = document.getElementById("no-todos")
        title_container.classList.add("hidden")
        todo_container.classList.add("hidden")
        no_todos_elem.classList.remove("hidden")
    }
}