jQuery(document).ready(function () {
	jQuery('.mod-main h2').toggle(
		function () {
			jQuery(this).siblings().animate({ height: 'hide', opacity: 'hide' }, 'slow');
		}, function () {
			jQuery(this).siblings().animate({ height: 'show', opacity: 'show' }, 'slow');
		}
	);
});