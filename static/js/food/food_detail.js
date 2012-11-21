var j = jQuery.noConflict();
j(document).ready(function () {
	// hide string content in brief content of the part more than length = 50
	var $bContent = j('p.brief-intro').text();
	var bLength = $bContent.length;
	if (bLength > 70) {
		// $clicedRemaining = $bContent.slice(100);
		$slicedContent = $bContent.slice(0, 100) + '...&nbsp;&nbsp;&nbsp;' + '<a href="#">Show more</a>';
		j('p.brief-intro').html($slicedContent);
		// alert($bContent);
	}
	j('p.brief-intro a').toggle(
		function () {
			$showContent = $bContent + '...&nbsp;&nbsp;&nbsp;' + '<a href="#">Hide</a>';
			j('p.brief-intro').html($showContent);
		}, function() {
			$slicedContent = $bContent.slice(0, 100) + '...&nbsp;&nbsp;&nbsp;' + '<a href="#">Show more</a>';
			j('p.brief-intro').html($slicedContent);
	});
});