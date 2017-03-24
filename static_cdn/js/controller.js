$(function () {
	$window = $(window);

	var size = {
			width: $window.width(),
			height: $window.height()
		}

	//IMAGE LIQUID
    $(".lqd").imgLiquid();

    /*SLIDE HEADLINE*/
	$("#slide_headline").slick({
		arrows: false,
		autoplay: true,
		speed: 800,
		fade: true,
		cssEase: "linear",
		dots: true,
        infinite: true,
        adaptiveHeight: true
   	});

   	// SLIDE NGOPI BARENG
   	$('#slide_ngopi').slick({
	  	dots: false,
	  	infinite: true,
	  	speed: 400,
	  	cssEase: "linear",
	  	slidesToShow: 3,
	  	slidesToScroll: 1,
	  	adaptiveHeight: true,
	  	responsive: [
	    {
	      	breakpoint: 768,
	      	settings: {
	        	slidesToShow: 2,
	        	slidesToScroll: 1
	      	}
	    },
	    {
	      	breakpoint: 576,
	     	 settings: {
	        	slidesToShow: 1,
	        	slidesToScroll: 1
	      	}
	    }
	    // You can unslick at a given breakpoint now by adding:
	    // settings: "unslick"
	    // instead of a settings object
	  	]
	});

	$("#slide_ngopi .slick-list").wrap("<div class='slidenav_wrap'></div>");

	$("#menu_toggle").click(function() {
		$(this).toggleClass("menu_open");
	});

	var mq  =  window.matchMedia('(min-width: 768px)');
	var mq2 =  window.matchMedia('(min-width: 576px)');

    if (!/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) && mq2.matches) {

    	// do something

		//DROPDOWN MENU
		$(".dropdown").hover(
			function() {
				$(this).addClass("open");
			},
			function() {
				$(this).removeClass("open");	
		});

	} else {

		// do something

		//DROPDOWN MENU
		$(".dropdown").click(function(event){
			$(this).toggleClass("open");
			return false;
		});

	}

	if (mq2.matches) {
		$window.scroll(function() {
	        var windowpos = $window.scrollTop();
	        var navpos = $("#header").outerHeight();

	        if(windowpos >= navpos) {
	            $("#nav").addClass("fixed")
	        }
	        else {
	            $("#nav").removeClass("fixed");
	        }
	    });
	}

	$('li.dropdown ul').find('a').on('click', function() {
	    window.location = $(this).attr('href');
	});

	//Check to see if the window is top if not then display button
	$(window).scroll(function(){
		if ($(this).scrollTop() > 1000) {
			$('.scrollToTop').fadeIn(300);
		} else {
			$('.scrollToTop').fadeOut(300);
		}
	});
	
	//Click event to scroll to top
	$('.scrollToTop').click(function(){
		$('html, body').animate({scrollTop : 0},800);
		return false;
	});

	//SEARCH
	var hahay = document.body
	var morphSearch = document.getElementById( 'morphsearch' ),
	input = morphSearch.querySelector( 'input.morphsearch-input' ),
	ctrlClose = morphSearch.querySelector( 'span.morphsearch-close' ),
	isOpen = isAnimating = false,
	// show/hide search area
	toggleSearch = function(evt) {
		// return if open and the input gets focused
		if( evt.type.toLowerCase() === 'focus' && isOpen ) return false;

		var offsets = morphsearch.getBoundingClientRect();
		if( isOpen ) {
			classie.remove( morphSearch, 'open' );
			classie.remove( hahay, 'unscroll' );
			// $(this).siblings('.morphsearch-form').children('.morphsearch-input').removeAttr('placeholder');
			$(this).siblings('.morphsearch-content').css('height', 0);
			$(this).siblings('.morphsearch-content').children('.latest').children('.list').css('height', 0);

			// trick to hide input text once the search overlay closes 
			// todo: hardcoded times, should be done after transition ends
			if( input.value !== '' ) {
				setTimeout(function() {
					classie.add( morphSearch, 'hideInput' );
					setTimeout(function() {
						classie.remove( morphSearch, 'hideInput' );
						input.value = '';
					}, 300 );
				}, 500);
			}
			
			input.blur();

			// pageurl = $('#search-keyword').attr('data-urlBack');
   //          console.log(pageurl);

   //          if(pageurl!=window.location){
   //              window.history.pushState({path:pageurl},'',pageurl);
   //          }
		}
		else {
			classie.add( morphSearch, 'open' );
			classie.add( hahay, 'unscroll' );
			// $(this).attr('placeholder', 'Enter keyword');
		}
		isOpen = !isOpen;
		
	};

	// events
	input.addEventListener( 'focus', toggleSearch );
	ctrlClose.addEventListener( 'click', toggleSearch );
	// esc key closes search overlay
	// keyboard navigation events
	document.addEventListener( 'keydown', function( ev ) {
		var keyCode = ev.keyCode || ev.which;
		if( keyCode === 27 && isOpen ) {
			toggleSearch(ev);
		}
	} );
	
	/***** for demo purposes only: don't allow to submit the form *****/
	// morphSearch.querySelector( 'button[type="submit"]' ).addEventListener( 'click', function(ev) { ev.preventDefault(); } );

});