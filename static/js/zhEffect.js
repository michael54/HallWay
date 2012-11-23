$(document).ready(function () {
	$(window).scroll(function(){
        if ($(this).scrollTop() > 100) {
            $('a.scroll-up').fadeIn();
        } else {
            $('a.scroll-up').fadeOut();
        }
    }); 

    $('a.scroll-up').click(function(){
        $("html, body").animate({ scrollTop: 0 }, 600);
        return false;
    });
});