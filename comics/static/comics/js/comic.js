const reverse_chapter_list = () => {
  const chapter_list = $("#chapter-list li");
  const chapter_array = Array.prototype.slice.call(chapter_list);
  chapter_array.forEach((chapter) => {
    chapter.parentNode.insertBefore(chapter, chapter.parentNode.firstChild);
  });
}

const showBuyModal = (chapter_id) => {
  $("#buyForm #buyValue").val(chapter_id);
  $("#buyModal").modal("show");
}

$('#buyForm').submit((e) => {
  e.preventDefault();
  const chapter_id = $("#buyForm #buyValue").val();
  console.log(chapter_id);
  $.ajax({
    url: `/comics/buy_chapter/${chapter_id}`,
    type: 'POST',
    headers: {
      'X-CSRFToken': csrftoken
    },
    success: (data) => {
      $("#buyModal").modal("hide");
      data = JSON.parse(data);
      alert(data['message']);
      location.reload();
    }
  })
})

const deleteChapter = (chapter_id) => {
  $.ajax({
    url: `/comics/delete_chapter/${chapter_id}/`,
    type: 'DELETE',
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
  })
}