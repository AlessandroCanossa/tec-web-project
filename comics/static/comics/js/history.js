const deleteHistoryEntry = (id) => {
  $.ajax({
    url: `/comics/delete_history_entry/${id}`,
    type: 'DELETE',
    headers: {
      'X-CSRFToken': csrftoken
    },
    success: (data) => {
      location.reload();
    }
  })
}