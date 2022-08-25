/**--- Delete a todo  ---**/
const deleteBtn = document.querySelectorAll('.delete-task')
.forEach(elt => {
  elt.onclick = e => {
    const todoId = e.target.dataset['id'];
    const deleted = true
    fetch('/todos/' + todoId + '/delete_todo', {
      method: 'DELETE',
      body: JSON.stringify({
        'deleted' : deleted
      }),
      headers:({
        'Content-Type' : 'application/json'
      })
    })
    .then(function() {
      document.getElementById('error').className = 'hidden';
      elt.parentNode.remove();
    })
    .catch(function() {
      document.getElementById('error').className = '';
    })
  }

})

/**--- Completed a todo  ---**/
const checkboxes = document.querySelectorAll('.check-completed');
for (let i = 0; i < checkboxes.length; i++) {
  const checkbox = checkboxes[i];
  checkbox.onchange = function(e) {
    const newCompleted = e.target.checked;
    const todoId = e.target.dataset['id'];
    fetch('/todos/' + todoId + '/set-completed', {
      method: 'POST',
      body: JSON.stringify({
        'completed': newCompleted
      }),
      headers: {
        'Content-Type': 'application/json'
      }
    })
    .then(function() {
      document.getElementById('error').className = 'hidden';
    })
    .catch(function() {
      document.getElementById('error').className = '';
    })
  }
}

/**--- Add a todo  ---**/
document.getElementById('form').onsubmit = e => {
  e.preventDefault();
  fetch('/todos/create', {
      method: 'POST',
      body: JSON.stringify({
          'description' : document.getElementById('description').value,
          'list_id' : document.getElementById('active_list').value
      }),
      headers: {
          'Content-Type': 'application/json'
      }
  })
  .then(function(response){
      return response.json();
  })
  .then(function(jsonResponse){
      const liItem = document.createElement('LI');
      liItem.innerHTML = jsonResponse['description'];
      const checkbox = document.createElement('input');
      checkbox.className = 'check-completed';
      checkbox.type = 'checkbox';
      checkbox.setAttribute('data-id', jsonResponse.id);
      liItem.appendChild(checkbox);
      console.log(jsonResponse);
      document.getElementById('todos').appendChild(liItem);
  })
  .catch(function(error){
      console.log(error)
  })
}