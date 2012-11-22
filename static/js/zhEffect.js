var j = jQuery.noConflict();

j(document).ready(function () {
	j(window).scroll(function(){
        if (j(this).scrollTop() > 100) {
            j('a.scroll-up').fadeIn();
        } else {
            j('a.scroll-up').fadeOut();
        }
    }); 

    j('a.scroll-up').click(function(){
        j("html, body").animate({ scrollTop: 0 }, 600);
        return false;
    });
});