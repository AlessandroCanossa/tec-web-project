const bttBtn = document.getElementById('backToTopBtn');

window.onscroll = function () {
  scrollFunction();
};

const scrollFunction = () => {
  if (
      document.body.scrollTop > 20 ||
      document.documentElement.scrollTop > 20
  ) {
    bttBtn.style.display = "block";
  } else {
    bttBtn.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
bttBtn.addEventListener("click", () => {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
});