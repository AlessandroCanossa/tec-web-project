const save_bookmark = (comic_id) => {
  $.ajax({
    url: '/comics/save_bookmark/' + comic_id,
    type: 'POST',
    success: function (data) {
      if (data.success) {
        $('#bookmark_').removeClass('btn-outline-primary').addClass('btn-primary');
      } else {
        alert(data.message);
      }
    }
  });
};

const rate_comic = (comic_id, rating) => {
  $.ajax({
    url: `/comics/rate_comic?c=${comic_id}&r=${rating}`,
    type: 'POST',
    success: function (data) {
      if (data.success) {
        $('#rating_').removeClass('btn-outline-primary').addClass('btn-primary');
      } else {
        alert(data.message);
      }
    }
  });
};