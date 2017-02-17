$(function () {

    if (($(window).width() >= 768) && ($(window).width() <= 1024)) {
        $('.masthead nav .masthead-nav > li > a').attr('href', 'javascript:void(0)');
    }

    $(document).ready(function(){
        $('.tovar-foto').slick({
            dots: true,
            infinite: true,
            speed: 300,
            slidesToShow: 1,
            adaptiveHeight: true
        });

    });

    resizeMinWidth();

    $(window).resize(resizeMinWidth);

    $(document).on('click', '#navbar-topmenu-mob .mobile-menu-close, .mobile-menu', function (e) {
        e.preventDefault();
        $('#navbar-topmenu-mob').toggleClass('active');
        $('#navbar-topmenu-mob').toggleClass('in');
        return false;
    });

    var Accordion = function(el, multiple) {
        this.el = el || {};
        this.multiple = multiple || false;

        // Variables privadas
        var links = this.el.find('.link');
        // Evento
        links.on('click', {el: this.el, multiple: this.multiple}, this.dropdown)
    }

    Accordion.prototype.dropdown = function(e) {
        var $el = e.data.el;
        $this = $(this),
            $next = $this.next();

        $next.slideToggle();
        $this.parent().toggleClass('open');

        if (!e.data.multiple) {
            $el.find('.submenu').not($next).slideUp().parent().removeClass('open');
        };
    }

    var accordion = new Accordion($('#accordion'), false);

});

function resizeMinWidth() {
    var $foot = $('.site-wrapper.homepage .mastfoot');

    if ($(window).width() <= 1185) {
        $foot.css({
            height: $foot.outerHeight() - 33 + 'px',
            top: $(window).height() - $foot.outerHeight() - 48 + 'px'
        });
    } else {
        $foot.attr('style', '');
    }

    $('.cover').css('margin-bottom', $foot.height() + 'px');

    if (!$('.cover .slider').hasClass('slick-initialized')) {
        $('.cover .slider').slick({
            dots: true,
            infinite: true,
            speed: 300,
            slidesToShow: 1,
            adaptiveHeight: true
        });
    }
}
