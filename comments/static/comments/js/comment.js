const removeReply = () => {
  $('#replyBox').hide();
  $('#replyId').val('');
}
const postReply = (commentId, username) => {
  $("#replyId").val(commentId);
  $('#replyBox').show();
  $("#replyTo").text(`Reply to ${username}`);
  $('#newComment').focus();
}

const deleteComment = (commentId) => {
  $.ajax({
    url: `/comments/delete/${commentId}`,
    type: 'DELETE',
    headers: {
      'X-CSRFToken': csrftoken
    },
    success: (data) => {
      location.reload();
    }
  });
}

