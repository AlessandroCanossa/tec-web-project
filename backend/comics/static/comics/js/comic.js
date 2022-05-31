const reverse_chapter_list = () => {
  const chapter_list = $("#chapter-list li");
  const chapter_array = Array.prototype.slice.call(chapter_list);
  chapter_array.forEach((chapter) => {
    chapter.parentNode.insertBefore(chapter, chapter.parentNode.firstChild);
  });
}

const showBuyModal = (chapter_id) => {
  $("#buyChapter")[0].href = `/comics/buy_chapter/${chapter_id}`;
  $("#buyModal").modal("show");
}