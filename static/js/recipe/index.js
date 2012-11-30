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

  var needResize = true;
  var resizeDiv = function () {
    dHeight = window.innerHeight;
    jQuery('ul.upper-level > li').css('top', dHeight*0.2);
    jQuery('a.show-control').css('top', dHeight*0.2+200);
    jQuery('ul.lower-level').css('top', dHeight*0.2+150);
    var dWidth = jQuery('li.show-item').width()*5;
    var dLeft = (window.innerWidth- dWidth)/2;
    jQuery('ul.lower-level').each(function () {
      jQuery(this).find('li').each(function (i) {
        jQuery(this).css('left', 144*i);
      });
    });
    if (needResize){
      jQuery('ul.upper-level > li').each(function (i) {
        jQuery(this).css('left', dLeft + 144*i);
      });
    }
    jQuery('ul.lower-level').css('left', dLeft);
    jQuery('a#pItem').css('left', dLeft-60);
    jQuery('a#nItem').css('left', dLeft+dWidth+40); 
    jQuery('ul.lower-level').css('width', 144*5);
    jQuery('ul.lower-level').css('height', jQuery('ul.lower-level > li > a').height()+10);
  }
  resizeDiv();
  jQuery(window).resize(resizeDiv);

  var move = 0;
  var showEffect = function (obj, event) {
    // obj.siblings().unbind(event);
    move = jQuery('ul.upper-level > li:nth-child(3)').position().left - jQuery(obj).position().left;
    jQuery('ul.upper-level > li').animate({
      'left': '+='+move
    }, {queue:false, duration: 1000, complete: function () {
      var dataTarget = jQuery(obj).attr('id');
      jQuery('ul.lower-level[data-target="'+dataTarget+'"]').show();
      var numChild = jQuery('ul.lower-level[data-target="'+dataTarget+'"]').children().length;
      if (numChild > 5) jQuery('a.show-control[href="#'+dataTarget+'"]').show();
      // obj.siblings().click(function() {showEffect(jQuery(this));});
    }});
    jQuery(obj).siblings().fadeOut(1000);
    jQuery('div.content.search-form').fadeOut(1000);
  };

  var hideEffect = function (obj, event) {
    // obj.siblings().unbind(event);
    var dataTarget = jQuery(obj).attr('id');
    jQuery('ul.lower-level[data-target="'+dataTarget+'"]').hide();
    jQuery('a.show-control[href="#'+dataTarget+'"]').hide();
    jQuery('ul.upper-level > li').animate({
      'left': '-='+move
    }, {queue:false, duration: 1000, complete: function () {
      // obj.siblings().click(function() {hideEffect(jQuery(this));});
    }});
    jQuery(obj).siblings().fadeIn(1000);
    jQuery('div.content.search-form').fadeIn(1000);
  };

  jQuery('ul.upper-level > li:not(.hot)').toggle(
    function (event){
      showEffect(jQuery(this), event);
    },
    function (event){
      hideEffect(jQuery(this), event);
    }
  );

  var nextItem = function (obj, event) {
    obj.unbind(event);
    var val = obj.attr('href').slice(1);
    var numChild = jQuery('ul.lower-level > li[data-target="'+val+'"]').length;
    var $firstChild = jQuery('ul.lower-level > li[data-target="'+val+'"]').first();
    console.log($firstChild.html());
    // if (firstLeft == -1*(numChild-5)*144) {
    // jQuery('ul.lower-level > li[data-target="'+val+'"]').stop(true).animate({
    //   'left': '+='+(numChild-5)*144
    // }, {queue: false, duration: 500, complete: function () {
    //   obj.click(function() {nextItem(obj);});
    // }});
    // } else {
    jQuery('ul.lower-level > li[data-target="'+val+'"]').stop(true).animate({
      'left': '-=144'
    }, {queue: false, duration: 500, complete: function () {
      obj.click(function() {nextItem(obj);});
      $firstChild.css('left', $firstChild.position().left+144*numChild);
      jQuery('ul.lower-level[data-target="'+val+'"]').append($firstChild);
      $firstChild.remove();
      // console.log(jQuery('ul.lower-level[data-target="'+val+'"]').last().html());
      // console.log(jQuery('ul.lower-level[data-target="'+val+'"]').first().html());
    }});
    // }
  }
  jQuery('a#nItem').click(function (event) {nextItem(jQuery(this), event);});
  var prevItem = function (obj, event) {
    obj.unbind(event);
    var val = obj.attr('href').slice(1);
    var numChild = jQuery('ul.lower-level > li[data-target="'+val+'"]').length;
    var firstLeft = jQuery('ul.lower-level > li[data-target="'+val+'"]').first().position().left;
    if (firstLeft == 0) {
      jQuery('ul.lower-level > li[data-target="'+val+'"]').stop(true).animate({
        'left': '-='+(numChild-5)*144
      }, {queue: false, duration: 500, complete: function () {
        obj.click(function() {prevItem(obj);});
      }});
    } else {
      jQuery('ul.lower-level > li[data-target="'+val+'"]').stop(true).animate({
        'left': '+=144'
      }, {queue: false, duration: 500, complete: function () {
        obj.click(function() {prevItem(obj);});
      }});
    }
  }
  jQuery('a#pItem').click(function (event) {prevItem(jQuery(this), event);});
});
