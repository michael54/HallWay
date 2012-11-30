function yuSlider(div, caption, time, prev, next){
  var iterNum = -1;
  var oldNum = 9;
  var intervalFunc = function (){
    iterNum = iterNum + 1;
    if(iterNum > 9){
      iterNum = 0;
    }
    oldNum = iterNum - 1;
    if(oldNum<0){
      oldNum = 9;
    }
    jQuery(div).eq(oldNum).fadeOut('slow');
    jQuery(div).eq(iterNum).fadeIn('slow');
    
  };

  intervalFunc();
  var interval = setInterval(intervalFunc, time);

  jQuery(prev).click(function() {
    oldNum = iterNum - 1;
    if(oldNum<0){
      oldNum = 9;
    }
    jQuery(div).eq(iterNum).fadeOut('slow');
    jQuery(div).eq(oldNum).fadeIn('slow');
    iterNum = oldNum;
  });

  jQuery(next).click(function() {
    oldNum = iterNum + 1;
    if(oldNum>9){
      oldNum = 0;
    }
    jQuery(div).eq(iterNum).fadeOut('slow');
    jQuery(div).eq(oldNum).fadeIn('slow');
    iterNum = oldNum;
  });
  
  jQuery(div).hover(
      function () {
        clearInterval(interval);
        jQuery(this).find(caption).stop(true).fadeIn(400);
      }, function () {
        interval = setInterval(intervalFunc, time);
        jQuery(this).find(caption).stop(true).fadeOut(400);
      }
    );
}
