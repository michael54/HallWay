function yuEffect( yuDiv, yuImg, time ){
	window.onload = function() {
		var pic_real_height;
		pic_real_height = yuImg.height();
		
		var divHeight = yuDiv.height();
		yuImg.css("margin-top", (divHeight - pic_real_height)/2);


		yuDiv.toggle(function(){
		  yuDiv.animate({
		    height: pic_real_height,

		  }, time);
		  yuImg.animate({
		  	marginTop: '0px',
		  }, time);

		}, function(){
			yuDiv.animate({
		    height: divHeight,

		  }, time);
		  yuImg.animate({
		  	marginTop: (divHeight - pic_real_height)/2,
		  }, time);
		});
	};
};