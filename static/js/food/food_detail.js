var j = jQuery.noConflict();
j(document).ready(function () {
	// hide string content in brief content of the part more than length = 50
	var $bContent = j('div.brief-intro').text();
	var bLength = $bContent.length;
	if (bLength > 70) {
		// $clicedRemaining = $bContent.slice(100);
		$slicedContent = $bContent.slice(0, 100) + '...   ';
		j('div.brief-intro').text($slicedContent);
		j('a.hide-show').show();
		// alert($bContent);
	}
	j('a.hide-show').toggle(
		function () {
			$showContent = $bContent;
			j('div.brief-intro').text($showContent);
			j('a.hide-show').text('Hide');
		}, function() {
			$slicedContent = $bContent.slice(0, 100) + '...   ';
			j('div.brief-intro').html($slicedContent);
			j('a.hide-show').text('Show more');
	});
});