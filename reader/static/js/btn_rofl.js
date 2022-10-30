$(document).on('mousemove', function (e) {
    $('#btn-lol').css({
        marginLeft: -e.pageX / 100 + 20,
        marginTop: -e.pageY / 100 + 20
    })
})

// function getRandomInt(min, max) {
//     return Math.floor(Math.random() * (max - min + 1)) + min;
// }
// function newPosition (oldTop, oldLeft, width, height) {
//     var range = 2; // Тут выставьте свой минимальный диапазон дальности
//     var newTop = getRandomInt(0, height);
//     var newLeft = getRandomInt(0, width);
//     if ( ((oldTop-range)<newTop && (oldTop+range)>newTop) ||
//          ((oldLeft-range)<newLeft && (oldLeft+range)>newLeft)) 
//        return newPosition (oldTop, oldLeft, width, height);
//     else return [newTop, newLeft];
// }
// $("#my-button").hover(function () {
//     var buttonPosition = newPosition ( 
//         parseInt($(this).css("top")), 
//         parseInt($(this).css("left")), 
//         $(".button-wrapper").width(), 
//         $(".button-wrapper").height() 
//     );
//     $(this).css({
//         top: buttonPosition[0],
//         left: buttonPosition[1]
//     });
// }, function () { });



// второй вариант
function getRandomInt(min, max) {
return Math.floor(Math.random() * (max - min + 1)) + min;
}
$("#btn-lol").hover(function () { 
$(this).css({
    top: getRandomInt(0, 500)+"px",
    left: getRandomInt(0, 500)+"px"
});
}, function () { });