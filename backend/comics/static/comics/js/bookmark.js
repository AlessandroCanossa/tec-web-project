const removeBookmark = (comic_id) => {
  $.ajax({
    url: '/comics/toggle_bookmark/' + comic_id,
    type: 'DELETE',
    headers: {
      'X-CSRFToken': csrftoken
    },
    success: () => {
      location.reload();
    }
  });
}

const addBookmark = (comic_id) => {
  $.ajax({
    url: '/comics/toggle_bookmark/' + comic_id,
    type: 'POST',
    headers: {
      'X-CSRFToken': csrftoken
    },
    success: () => {
      location.reload();
    }
  });
}