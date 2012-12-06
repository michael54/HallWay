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

  jQuery('ul.did-show-inner > li > a').stop().hover(function () {
  	jQuery(this).find('div.did-show-caption').stop().fadeIn(500);
    return false;
  }, function () {
  	jQuery(this).find('div.did-show-caption').stop().fadeOut(500);
    return false;
  });

  jQuery('div.rat-content div').each(function (i) {
    var $bContent = jQuery(this).text();
    var t = jQuery(this);
    var bLength = $bContent.length;
    if (bLength > 100) {
      // $clicedRemaining = $bContent.slice(100);
      $slicedContent = $bContent.slice(0, 140) + '...   ';
      jQuery(t).text($slicedContent);
      jQuery(t).siblings('a.hide-show').show();
      jQuery(t).siblings('a.hide-show').toggle(
        function () {
          $showContent = $bContent;
          jQuery(t).text($showContent);
          jQuery(this).text('Hide');
          return false;
        }, function() {
          $slicedContent = $bContent.slice(0, 140) + '...   ';
          jQuery(t).html($slicedContent);
          jQuery(this).text('Show more');
          return false;
      });
      // alert($bContent);
    }
  })
  // hide string content in brief content of the part more than length = 50
  
  
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