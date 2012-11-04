var slide_effect = 'fade';
var slide_direction = 'N';
var slide_mode = 'normal';

$(document).ready(function(){
	
	bindEvents();
		
});

function bindEvents(){
	
	// set options 
	if (slide_effect == 'fade' || slide_effect == 'none') {
		hideObject($('.slide-directions'), 'slide')
	} else {
		if (slide_effect == 'simpleSlide') {
			hideObject($('.mode-randome'), 'none');
			if (slide_mode == 'random') slide_mode = 'normal';	
			if ($('INPUT.direction').index($("INPUT#dir-"+slide_direction.toLowerCase()+"")) > 3) {
				slide_direction = 'N';
			}
			
		} else showObject($('.mode-randome'), 'none'); 

		showObject($('.slide-directions'), 'slide');
		
		if (slide_effect == 'superSlide') showObject($('.super-directions'), 'none'); 
			else hideObject($('.super-directions'), 'none');
	}
		
	if (slide_mode == 'random') {	
		$('#nav').html('');
		hideObject($('.nav-buttons'), 'fade');
	} else showObject($('.nav-buttons'), 'fade');
		
	$('#toggleAnimation').html("Pause Animation");
	
	$("select#effect option[value='"+slide_effect+"']").attr("selected", true);
	$("INPUT#dir-"+slide_direction.toLowerCase()+"").attr('checked', 'checked');
	$("INPUT#"+slide_mode+"").attr('checked', 'checked');

	// Play / pause button
	$('#toggleAnimation').unbind('click');
	$('#toggleAnimation').click(function(){
		if ($(this).html() == "Pause Animation"){
			$(this).html("Resume Animation");
			$('BODY').bgStretcher.pause();
		} else {
			$(this).html("Pause Animation");
			$('BODY').bgStretcher.play();
		}
	});
	
	// Change Effect
	$('SELECT#effect').unbind('change');
	$('SELECT#effect').change(function(){
		if ($(this).val() == slide_effect) return true;
		slide_effect = $(this).val();
		$('BODY').bgStretcher.sliderDestroy();
		initBgStretcher();
		bindEvents();
		return true;
	});
	
	// Change Direction
	$('INPUT.direction').unbind('change');
	$('INPUT.direction').change(function(){	
		var new_slide_deriction = $('INPUT.direction:checked').attr('id').split('dir-');
		new_slide_deriction = new_slide_deriction[1].toUpperCase();

		if (new_slide_deriction == slide_direction)	return true;
		slide_direction = new_slide_deriction;

		$('BODY').bgStretcher.sliderDestroy();
		initBgStretcher();
		bindEvents();
		return true;
	});
	
	// Change Mode
	$('INPUT.mode').unbind('change');
	$('INPUT.mode').change(function(){	
		if ($(this).attr('id') == slide_mode) return true;
		slide_mode = $(this).attr('id');

		$('BODY').bgStretcher.sliderDestroy();
		initBgStretcher();
		bindEvents();
		return true;
	});
	
	return true;
}

function initBgStretcher(){

	$('BODY').bgStretcher({
		images: ['/static/img/bg-food1.jpg', '/static/img/bg-food2.jpg',
				'/static/img/bg-food3.jpg', '/static/img/bg-food4.jpg'],
		imageWidth: 1024, 
		imageHeight: 768, 
		slideDirection: slide_direction,
		slideShowSpeed: 1000,
		transitionEffect: slide_effect,
		sequenceMode: slide_mode,
		buttonPrev: '#prev',
		buttonNext: '#next',
		pagination: '#nav',
		anchoring: 'left center',
		anchoringImg: 'left center'
	});
}


function hideObject(obj, hide_effect) {
	if (($.browser.msie) && (parseInt(jQuery.browser.version) == 6)) {
			obj.css({position: 'absolute', left: '-100000px'});
		} else {
			if (hide_effect == 'slider') obj.slideUp();
				else  if (hide_effect == 'fade') obj.fadeOut();
					else obj.hide();
		}
	return true;
}
function showObject(obj, hide_effect) {
	if (($.browser.msie) && (parseInt(jQuery.browser.version) == 6)) {
			obj.css({position: 'static', left: '0px'});
		} else {
			if (hide_effect == 'slider') obj.slideDown();
				else  if (hide_effect == 'fade') obj.fadeIn();
					else obj.show();
		}
	return true;
} 