$(window).scroll(function () {
    if ($(window).scrollTop() >= 250) {
        $('#navbar-ul').css('background-color','#333');
    } 
    else {
        $('#navbar-ul').css('background-color','transparent');
    }
    if ($(window).scrollTop() >= 250) {
        $('#meniu li a').css('color','white');
        $('#meniu .dropdown-content').css('background-color','#333');
    } 
    else {
        $('#meniu li a').css('color','#00ffff');
        $('#meniu .dropdown-content').css('background-color','transparent');
    }
    
});