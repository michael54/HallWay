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

  var resizeDiv = function () {
    dHeight = window.innerHeight;
    jQuery('ul.upper-level > li').css('top', dHeight*0.2);
    jQuery('a.show-control').css('top', dHeight*0.2+200);
    // jQuery('ul.circular-show-inner.lower-level > li').css('top', dHeight*0.4);
    jQuery('ul.lower-level').css('top', dHeight*0.2+150);
    var dWidth = jQuery('li.show-item').width()*5;
    var dLeft = (window.innerWidth- dWidth)/2;
    jQuery('ul.lower-level > li').each(function (i) {
      jQuery(this).css('left', 144*i);
    });
    jQuery('ul.lower-level').css('left', dLeft);
    jQuery('a#pItem').css('left', dLeft-60);
    jQuery('a#nItem').css('left', dLeft+dWidth+20);
    jQuery('ul.upper-level > li#item1').css('left', dLeft);
    jQuery('ul.upper-level > li#item2').css('left', dLeft+144);
    jQuery('ul.upper-level > li#item3').css('left', dLeft+144*2);
    jQuery('ul.upper-level > li#item4').css('left', dLeft+144*3);
    jQuery('ul.upper-level > li#item5').css('left', dLeft+144*4);
    jQuery('ul.lower-level').css('width', dWidth);
    jQuery('ul.lower-level').css('height', jQuery('ul.lower-level > li >a').height());
  }
  resizeDiv();
  jQuery(window).resize(resizeDiv);

  var move = 0;
  jQuery('li.show-item').toggle(function () {
    move = jQuery('li#item3').position().left - jQuery(this).position().left;
    // console.log(move);
    jQuery('ul.circular-show-inner.upper-level > li').animate({
      'left': '+='+move
    }, {queue:false, duration: 1000, complete: function () {
      jQuery('.lower-level').show();
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
