const addRating = (id, rating) => {
  $.ajax({
    url: `/comics/rate_comic/${id}/${rating}`,
    type: 'POST',
    headers: {
      'X-CSRFToken': csrftoken
    },
    success: (data) => {
      location.reload();
    }
  })
}

const modifyRating = (id, rating) => {
  $.ajax({
    url: `/comics/rate_comic/${id}/${rating}`,
    type: 'PUT',
    headers: {
      'X-CSRFToken': csrftoken
    },
    success: (data) => {
      location.reload();
    }
  })
}

const removeRating = (id) => {
  $.ajax({
    url: `/comics/rate_comic/${id}/0`,
    type: 'DELETE',
    headers: {
      'X-CSRFToken': csrftoken
    },
    success: (data) => {
      location.reload();
    }
  })
}