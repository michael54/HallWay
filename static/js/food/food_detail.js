jQuery(document).ready(function () {
	// hide string content in brief content of the part more than length = 50
	var $bContent = jQuery('div.brief-intro div').text();
	var bLength = $bContent.length;
	if (bLength > 70) {
		// $clicedRemaining = $bContent.slice(100);
		$slicedContent = $bContent.slice(0, 100) + '...   ';
		jQuery('div.brief-intro div').text($slicedContent);
		jQuery('a.hide-show').show();
		// alert($bContent);
	}
	jQuery('a.hide-show').toggle(
		function () {
			$showContent = $bContent;
			jQuery('div.brief-intro div').text($showContent);
			jQuery('a.hide-show').text('Hide');
		}, function() {
			$slicedContent = $bContent.slice(0, 100) + '...   ';
			jQuery('div.brief-intro div').html($slicedContent);
			jQuery('a.hide-show').text('Show more');
	});
});