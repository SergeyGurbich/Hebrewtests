var slideIndex = 1;

function showSlider() {
  document.getElementById("slider").style.display = "block";
  showSlide(slideIndex);
}

function nextSlide() {
  showSlide(slideIndex += 1);
}

function prevSlide() {
  showSlide(slideIndex -= 1);
}

function showSlide(n) {
  var slides = document.getElementsByClassName("slider-image");
  if (n > slides.length) {
    slideIndex = 1;
  }
  if (n < 1) {
    slideIndex = slides.length;
  }
  for (var i = 0; i < slides.length; i++) {
    slides[i].classList.remove("active");
  }
  slides[slideIndex-1].classList.add("active");
}
