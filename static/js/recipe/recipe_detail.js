jQuery(document).ready(function () {
	jQuery('.mod-main h2').toggle(
		function () {
			jQuery(this).siblings().animate({ height: 'hide', opacity: 'hide' }, 'slow');
		}, function () {
			jQuery(this).siblings().animate({ height: 'show', opacity: 'show' }, 'slow');
		}
	);

	jQuery('ul.did-show-inner').each(function () {
    var numChild = jQuery(this).find('li').length;
    if (numChild > 3){
      jQuery(jQuery(this).find('li:first')).before(jQuery(jQuery(this).find('li:last')));
      jQuery('a.did-show-control').show();
    }
    else {
    	jQuery('div.did-show-outer').css('margin-left', 25);
      jQuery(jQuery(this).find('li:first')).before(jQuery(jQuery(this).find('li:last')).clone(false));
      jQuery('a.did-show-control').hide();
    }
  });

  jQuery('a#nItem').click(function (event) {slideControl('right' ,jQuery(this), event); return false;});
  jQuery('a#pItem').click(function (event) {slideControl('left' ,jQuery(this), event); return false;});

  jQuery('ul.did-show-inner > li > a').hover(function () {
  	jQuery(this).find('div.did-show-caption').fadeIn(500);
  }, function () {
  	jQuery(this).find('div.did-show-caption').fadeOut(500);
  });
});

/* the slide control function */ 
function slideControl(direction, obj, event){
  obj.unbind(event);
  var itemWidth = jQuery('ul.did-show-inner li').outerWidth();  

  if(direction == 'left'){
      var leftIndent = parseInt(jQuery('ul.did-show-inner').css('left')) + itemWidth;  
  }else{ 
      var leftIndent = parseInt(jQuery('ul.did-show-inner').css('left')) - itemWidth;  

  }  

  jQuery('ul.did-show-inner').animate({
    'left' : leftIndent
  },{queue: false, duration: 500, complete: function(){
    if(direction == 'left'){
      obj.click(function (event) {slideControl('left' ,jQuery(this), event); return false;});
      jQuery(jQuery('ul.did-show-inner > li').first()).before(
          jQuery(jQuery('ul.did-show-inner > li').last()));  
    }else{
      obj.click(function (event) {slideControl('right' ,jQuery(this), event); return false;});
      jQuery(jQuery('ul.did-show-inner > li').last()).after(
          jQuery(jQuery('ul.did-show-inner > li').first())); 
    }

    jQuery('ul.did-show-inner').css({'left' : '-151px'});  
  }});   
}