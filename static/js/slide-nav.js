var currentSlideIndex = 1;
var currentSlideIndexInstr = 1;

function plusSlides(n) {
    currentSlideIndex += n
    showSlides(currentSlideIndex);
}

function currentSlide(n) {
    currentSlideIndex = n
    showSlides(currentSlideIndex);
}

function showSlides(n) {
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("dot");
    // Efectul de continuitate a pozelor
    if (n > slides.length) {
        currentSlideIndex = 1
    }    
    if (n < 1) {
        currentSlideIndex = slides.length
    }
    var i = 0;
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active-car", "");
    }
    
    slides[currentSlideIndex-1].style.display = "block";
    dots[currentSlideIndex-1].className += " active-car";
}

function plusSlidesInstr(n) {
    currentSlideIndexInstr += n
    showSlidesInstr(currentSlideIndexInstr);
}

function currentSlideInstr(n) {
    currentSlideIndexInstr = n
    showSlidesInstr(currentSlideIndexInstr);
}

function showSlidesInstr(n) {
    var slides = document.getElementsByClassName("mySlidesInstr");
    var dots = document.getElementsByClassName("dotInstr");
    // Efectul de continuitate a pozelor
    if (n > slides.length) {
        currentSlideIndexInstr = 1
    }    
    if (n < 1) {
        currentSlideIndexInstr = slides.length
    }
    var i = 0;
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active-car", "");
    }
    
    slides[currentSlideIndexInstr-1].style.display = "block";
    dots[currentSlideIndexInstr-1].className += " active-car";
}