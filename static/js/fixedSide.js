function fixedSide(str){
  var divH = jQuery(str).position().top;
  jQuery(window).scroll(function() {
    var position = jQuery(window).scrollTop();
    if (position>=divH){
      jQuery(str).css('padding-top', (position-divH)+'px');
    }
    else {
      jQuery(str).css('padding-top', '0');
    }
  });
}
  