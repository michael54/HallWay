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

  // index page recipe category show
  var pLeft = (window.innerWidth - j('a.show-item').width())/2;
  jQuery('a.show-item').click(function () {
    // console.log(jQuery(this).position().left);
    var ppleft = pLeft - jQuery(this).position().left;
    jQuery(this).parent().animate({
      left: ppleft
    }, 1000, function () {

    });
    jQuery(this).siblings().animate({
      opacity: 0.0
    }, 1000, function() {
      // Animation complete.
    });
  });
});
