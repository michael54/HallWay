var BlurBGImage	= (function() {
	
	var $bxWrapper			= $('#bx-wrapper'),
		// loading status to show while preloading images
		$bxLoading			= $bxWrapper.find('div.bx-loading'),
		// container for the bg images and respective canvas
		$bxContainer		= $bxWrapper.find('div.bx-container'),
		// the bg images we are gonna use
		$bxImgs				= $bxContainer.children('img'),
		// total number of bg images
		bxImgsCount			= $bxImgs.length,
		// current image's index
		current				= 0,
		// variation to show the image:
		// (1) - blurs the current one, fades out and shows the next image
		// (2) - blurs the current one, fades out, shows the next one (but initially blurred)
		// speed is the speed of the animation
		// blur Factor is the factor used in the StackBlur script
		animOptions			= { speed : 900, variation : 2, blurFactor : 20 },
		// control if currently animating
		isAnim				= false,
		// check if canvas is supported
		supportCanvas 		= Modernizr.canvas,
		// slideshow
		slideshow_interval	= 7000,
		slideshow_time,
		
		// init function
		init				= function() {
			
			// preload all images and respective canvas
			var loaded = 0;
			
			$bxImgs.each( function(i) {
				
				var $bximg	= $(this);
				
				// save the position of the image in data-pos
				$('<img data-pos="' + $bximg.index() + '"/>').load(function() {
					
					var $img	= $(this),
						// size of image to be fullscreen and centered
						dim		= getImageDim( $img.attr('src') ),
						pos		= $img.data( 'pos' );
					
					// add the canvas to the DOM
					$.when( createCanvas( pos, dim ) ).done( function() {
							
						++loaded;
						
						// all images and canvas loaded
						if( loaded === bxImgsCount ) {
							
							// apply style for bg image and canvas
							centerImageCanvas();
							
							// hide loading status
							$bxLoading.hide();
							
							// initialize events
							initEvents();
							
							// start slideshow
							startSlideshow();
							
						}
						
					});
				
				}).attr( 'src', $bximg.attr('src') );
			
			});
			
		},
		startSlideshow		= function() {
			
			slideshow_time = setTimeout( function() {
				
				if( !isAnim ) {
					
					var pos = current;
					( pos < bxImgsCount - 1 ) ? ++pos : pos = 0;
					isAnim = true;
					// show the bg image
					showImage( pos );
					startSlideshow();
				
				}
			
			}, slideshow_interval );
			
		},
		// creates the blurred canvas image
		createCanvas		= function( pos, dim ) {
			
			return $.Deferred( function(dfd) {
				
				// if canvas not supported return
				if( !supportCanvas ) {
					dfd.resolve();
					return false;
				}	
				
				// create the canvas element:
				// size and position will be the same like the fullscreen image
				var $img	= $bxImgs.eq( pos ),
					imgW	= dim.width,
					imgH	= dim.height,
					imgL	= dim.left,
					imgT	= dim.top,
					
					canvas	= document.createElement('canvas');
				
				canvas.className		= 'bx-canvas';
				canvas.width 			= imgW;
				canvas.height 			= imgH;
				canvas.style.width  	= imgW + 'px';
				canvas.style.height 	= imgH + 'px';
				canvas.style.left		= imgL + 'px';
				canvas.style.top		= imgT + 'px';
				canvas.style.visibility = 'hidden';
				// save position of canvas to know which image this is linked to
				canvas.setAttribute('data-pos', pos);
				// append the canvas to the same container where the images are
				$bxContainer.append( canvas );
				// blur it using the StackBlur script
				stackBlurImage( $img.get(0), dim, canvas, animOptions.blurFactor, false, dfd.resolve );
			
			}).promise();
				
		},
		// gets the image size and position in order to make it fullscreen and centered.
		getImageDim			= function( img ) {
			
			var $img    = new Image();
			
			$img.src    = img;
			
			var $win	= $( window ),
				w_w		= $win.width(),
				w_h		= $win.height(),
				r_w		= w_h / w_w,
				i_w		= $img.width,
				i_h		= $img.height,
				r_i		= i_h / i_w,
				new_w, new_h, new_left, new_top;
					
			if( r_w > r_i ) {
				
				new_h	= w_h;
				new_w	= w_h / r_i;
			
			}
			else {
			
				new_h	= w_w * r_i;
				new_w	= w_w;
			
			}
					
			return {
				width	: new_w,
				height	: new_h,
				left	: ( w_w - new_w ) / 2,
				top		: ( w_h - new_h ) / 2
			};
		
		},
		// initialize the events
		initEvents			= function() {
			
			$( window ).on('resize.BlurBGImage', function( event ) {
				
				// apply style for bg image and canvas
				centerImageCanvas();
				return false;
				
			});
			
		},
		// apply style for bg image and canvas
		centerImageCanvas	= function() {
			
			$bxImgs.each( function(i) {
				
				var $bximg	= $(this),
					dim			= getImageDim( $bximg.attr('src') ),
					$currCanvas	= $bxContainer.children('canvas[data-pos=' + $bximg.index() + ']'),
					styleCSS	= {
						width	: dim.width,
						height	: dim.height,
						left	: dim.left,
						top		: dim.top
					};	
				
				$bximg.css( styleCSS );
				
				if( supportCanvas )
					$currCanvas.css( styleCSS );
					
				if( i === current )	
					$bximg.show();
				
			});
			
		},
		// shows the image at position "pos"
		showImage			= function( pos ) {
				
				// current image 
			var $bxImage		= $bxImgs.eq( current );
				// current canvas
				$bxCanvas		= $bxContainer.children('canvas[data-pos=' + $bxImage.index() + ']'),
				// next image to show
				$bxNextImage	= $bxImgs.eq( pos ),
				// next canvas to show
				$bxNextCanvas	= $bxContainer.children('canvas[data-pos='+$bxNextImage.index()+']');
			
			// if canvas is supported
			if( supportCanvas ) {
				
				$bxCanvas.css( 'z-index', 100 ).css('visibility','visible');
				
				$.when( $bxImage.fadeOut( animOptions.speed ) ).done( function() {
					
					switch( animOptions.variation ) {
					
						case 1 	:
							$.when( $bxNextImage.fadeIn( animOptions.speed ) ).done( function() {
						
								$bxCanvas.css( 'z-index', 1 ).css('visibility','hidden');
								current = pos;
								$bxNextCanvas.css('visibility','hidden');
								isAnim 	= false;
							
							});
							break;
						case 2	:
							$bxNextCanvas.css('visibility','visible');
							
							$.when( $bxCanvas.fadeOut( animOptions.speed * 1.5 ) ).done( function() {
							
								$(this).css({
									'z-index' 		: 1,
									'visibility'	: 'hidden'
								}).show();
								
								$.when( $bxNextImage.fadeIn( animOptions.speed ) ).done( function() {
									
									current = pos;
									$bxNextCanvas.css('visibility','hidden');
									isAnim 	= false;
								
								});
								
							});
							break;
					
					};
					
				});
			
			}
			// if canvas is not shown just work with the bg images
			else {
			
				$.when( $bxNextImage.css( 'z-index', 102 ).fadeIn( animOptions.speed ) ).done( function() {
					
					current = pos;
					$bxImage.hide();
					$(this).css( 'z-index', 101 );
					isAnim = false;
				
				});
			
			}
		
		};
		
	return {
		init	: init
	};

})();