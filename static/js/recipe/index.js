jQuery(document).ready(function () {
	
    // hover caption effect
    jQuery('a.ca-img-link .carousel1-caption').hide();
    jQuery('a.ca-img-link').unbind('hover');
    jQuery('a.ca-img-link').hover(
      function () {
        jQuery(this).children('.carousel1-caption').fadeIn('slow');
      }, function () {
        jQuery(this).children('.carousel1-caption').fadeOut('slow');
      }
    );
});
