// ### MAKE DICE SHOW IN INTERVALS ###

$(document).ready(function() {
    $("#h1, #h2, #h3, #h4, #h5, #h6, #hero_log_text").hide();
    timer = setTimeout(function () {
        $('#h1').show();
    }, 800);
    timer = setTimeout(function () {
        $('#h2').show();
    }, 1600);
    timer = setTimeout(function () {
        $('#h3').show();
    }, 2400);
    timer = setTimeout(function () {
        $('#h4').show();
    }, 3200);               
    timer = setTimeout(function () {
        $('#h5').show();
    }, 4000);
    timer = setTimeout(function () {
        $('#h6').show();
    }, 4800);
    timer = setTimeout(function () {
        $('#hero_log_text').show();
    }, 5600);
});


$(document).ready(function() {
    $("#e1, #e2, #e3, #e4, #e5, #e6, #enemy_log_text").hide();
    timer = setTimeout(function () {
        $('#e1').show();
    }, 800);
    timer = setTimeout(function () {
        $('#e2').show();
    }, 1600);
    timer = setTimeout(function () {
        $('#e3').show();
    }, 2400);
    timer = setTimeout(function () {
        $('#e4').show();
    }, 3200);               
    timer = setTimeout(function () {
        $('#e5').show();
    }, 4000);
    timer = setTimeout(function () {
        $('#e6').show();
    }, 4800);
    timer = setTimeout(function () {
        $('#enemy_log_text').show();
    }, 5600);
});