j(document).ready(function () {
	j('.mod-main h2').toggle(
		function () {
			j(this).siblings().animate({ height: 'hide', opacity: 'hide' }, 'slow');
		}, function () {
			j(this).siblings().animate({ height: 'show', opacity: 'show' }, 'slow');
		}
	);
});