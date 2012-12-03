jQuery(document).ready(function () {
	jQuery(window).scroll(function(){
        if (jQuery(this).scrollTop() > 100) {
            jQuery('a.scroll-up').fadeIn();
        } else {
            jQuery('a.scroll-up').fadeOut();
        }
    });
    jQuery(window).scroll(function(){
        if (jQuery(this).scrollTop() + jQuery(this).height() == jQuery(document).height()) {
            jQuery('a.scroll-down').fadeOut();
        } else {
            jQuery('a.scroll-down').fadeIn();
        }
    }); 

    jQuery('a.scroll-up').click(function(){
        jQuery("html, body").animate({ scrollTop: 0 }, 600);
        return false;
    });
    jQuery('a.scroll-down').click(function(){
        jQuery("html, body").animate({ scrollTop: jQuery(document).height() }, 600);
        return false;
    });
});