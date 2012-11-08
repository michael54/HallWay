j(document).ready(function () {
	/*window.onload = function () {
		$('body').show();
		$('body').animate({
			//opacity: 0.5,
		}, 2000, function() {
			// change img
		});
	};
	*/
	/*$('body').bgStretcher({
		images: ['/static/img/bg-food1.jpg', '/static/img/bg-food2.jpg',
				'/static/img/bg-food3.jpg', '/static/img/bg-food4.jpg'],
		imageWidth: 1024, 
		imageHeight: 768, 
		//slideDirection: 'N',
		nextSlideDelay: 1000,
		slideShowSpeed: 1000,
		slideShow: true,
		transitionEffect: 'fade',
		sequenceMode: 'normal',
		//buttonPrev: '#prev',
		//buttonNext: '#next',
		pagination: '#nav',
		anchoring: 'left center',
		anchoringImg: 'left center'
	}).play();*/

	
    // hover caption effect
    j('a.ca-img-link .carousel1-caption').hide();
    j('a.ca-img-link').unbind('hover');
    j('a.ca-img-link').hover(
      function () {
        j(this).children('.carousel1-caption').fadeIn('slow');
      }, function () {
        j(this).children('.carousel1-caption').fadeOut('slow');
      }
    );
});
