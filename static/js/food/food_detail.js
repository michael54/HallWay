$(document).ready(function () {
	// hide string content in brief content of the part more than length = 50
	var $bContent = $('p.brief-intro').text();
	var bLength = $bContent.length;
	if (bLength >= 50) {
		// alert($('p.brief-intro').html());
		$slicedContent = $bContent.slice(0, 100) + '...&nbsp;&nbsp;&nbsp;' + '<a href="#">more</a>';
		$('p.brief-intro').html($slicedContent);
		// alert($bContent);

	}
});