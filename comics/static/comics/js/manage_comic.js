const deleteComic = (comicId) => {
  $.ajax({
    url: `/comics/${comicId}/delete/`,
    type: 'DELETE',
    headers: {
      'X-CSRFToken': csrftoken
    },
    success: (result) => {
      alert(result);
      location.reload()
    },
    error: (xhr, _ajaxOptions, _thrownError) => {
      alert(xhr.responseText);
    }
  })
}

const updateStatus = (statusId, comicId) => {
  $.ajax({
    url: `/comics/${comicId}/status/${statusId}/`,
    type: 'PUT',
    headers: {
      'X-CSRFToken': csrftoken
    },
    success: (result) => {
      alert(result);
      location.reload()
    },
    error: (xhr, _ajaxOptions, _thrownError) => {
      alert(xhr.responseText);
    }
  })
}