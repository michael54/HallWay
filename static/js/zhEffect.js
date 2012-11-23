jQuery(document).ready(function () {
	jQuery(window).scroll(function(){
        if (jQuery(this).scrollTop() > 100) {
            jQuery('a.scroll-up').fadeIn();
        } else {
            jQuery('a.scroll-up').fadeOut();
        }
    }); 

    jQuery('a.scroll-up').click(function(){
        jQuery("html, body").animate({ scrollTop: 0 }, 600);
        return false;
    });
});