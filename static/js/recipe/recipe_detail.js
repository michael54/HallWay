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

  // hide string content in brief content of the part more than length = 50
  var $bContent = jQuery('div.rat-content div').text();
  var bLength = $bContent.length;
  if (bLength > 140) {
    // $clicedRemaining = $bContent.slice(100);
    $slicedContent = $bContent.slice(0, 140) + '...   ';
    jQuery('div.rat-content div').text($slicedContent);
    jQuery('a.hide-show').show();
    // alert($bContent);
  }
  jQuery('a.hide-show').toggle(
    function () {
      $showContent = $bContent;
      jQuery('div.rat-content div').text($showContent);
      jQuery('a.hide-show').text('Hide');
    }, function() {
      $slicedContent = $bContent.slice(0, 140) + '...   ';
      jQuery('div.rat-content div').html($slicedContent);
      jQuery('a.hide-show').text('Show more');
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