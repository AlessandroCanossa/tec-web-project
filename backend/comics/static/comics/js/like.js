const addLike = (id) => {
  $.ajax({
    url: `/comics/like_chapter/${id}`,
    type: 'POST',
    headers: {
      'X-CSRFToken': csrftoken
    },
    success: (data) => {
      location.reload();
    }
  })
}
const removeLike = (id) => {
  $.ajax({
    url: `/comics/like_chapter/${id}`,
    type: 'Delete',
    headers: {
      'X-CSRFToken': csrftoken
    },
    success: (data) => {
      location.reload();
    }
  })
}