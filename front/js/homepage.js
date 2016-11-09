$(function () {
    $(document).ready(function(){
        $('.tovar-foto').slick({
            dots: true,
            infinite: true,
            speed: 300,
            slidesToShow: 1,
            adaptiveHeight: true
    });
    });

    $('.cover .slider').slick({
        dots: true,
        infinite: true,
        speed: 300,
        slidesToShow: 1,
        adaptiveHeight: true
    });

    resizeMinWidth();

    $(window).resize(resizeMinWidth);
});

function resizeMinWidth() {
    var $foot = $('.site-wrapper.homepage .mastfoot');

    if ($(window).width() <= 1185) {
        $foot.css({
            top: $(window).height() - $foot.outerHeight() - 650 + 'px'
        });
    } else {
        $foot.attr('style', '');
    }
}
