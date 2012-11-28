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
  // var pLeft = jQuery('li#item3').position().left;
  // console.log(pLeft);
  var move = 0;
  jQuery('li.show-item').toggle(function () {
    move = jQuery('li#item3').position().left - jQuery(this).position().left;
    console.log(move);
    jQuery('ul.circular-show-inner.upper-level > li').animate({
      'left': '+='+move
    }, {queue:false, duration: 1000, complete: function () {
      jQuery('ul.circular-show-inner.lower-level > li').show();
    }});
    jQuery(this).siblings().fadeOut(1000);
    jQuery('div.content.search-form').fadeOut(1000);
  }, function () {
    jQuery('ul.circular-show-inner.lower-level > li').hide();
    jQuery('ul.circular-show-inner.upper-level > li').animate({
      'left': '-='+move
    }, {queue:false, duration: 1000, complete: function () {
    }});
    jQuery(this).siblings().fadeIn(1000);
    jQuery('div.content.search-form').fadeIn(1000);
  });
});
