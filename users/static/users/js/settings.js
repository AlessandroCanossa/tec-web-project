$('#change-username').submit((e) => {
  e.preventDefault();
  const username = $('#new-username').val();
  $.ajax({
    url: '/users/change_username/',
    type: 'POST',
    data: {
      'username': username
    },
    headers: {
      'X-CSRFToken': csrftoken
    },
    success: (data) => {
      alert(data);
      location.reload();
    },
    error: (xhr, _ajaxOptions, _thrownError) => {
      alert(xhr.responseText);
    }
  });
})

$('#change-password').submit((e) => {
  e.preventDefault();
  const old_password = $('#old_password').val();
  const new_password = $('#new_password').val();
  const confirm_password = $('#confirm_password').val();

  console.log(old_password, new_password, confirm_password);

  $.ajax({
    url: '/users/change_password/',
    type: 'POST',
    data: {
      'old_password': old_password,
      'new_password': new_password,
      'confirm_password': confirm_password
    },
    headers: {
      'X-CSRFToken': csrftoken
    },
    success: (data) => {
      alert(data);
      location.reload();
    },
    error: (xhr, _ajaxOptions, _thrownError) => {
      alert(xhr.responseText);
    }
  });
})

const becomeCreator = () => {
  $.ajax({
    url: '/users/become_creator/',
    type: 'POST',
    headers: {
      'X-CSRFToken': csrftoken
    },
    success: (data) => {
      alert(data);
      location.reload();
    },
    error: (xhr, _ajaxOptions, _thrownError) => {
      alert(xhr.responseText);
    }
  });
}
