var breakingStart = true; // autostart breaking news
var breakingSpeed = 40; // breaking msg speed

var breakingScroll = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
var breakingOffset = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
var elementsToClone = [true, true, true, true, true, true, true, true, true, true];
var elementsActive = [];
var theCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0];

(function ($) {
    "use strict";

    function ot_Slider_move(itemid) {
        var thisel = itemid, currentb = thisel.parent().parent().children(".ot-slides").children(".ot-slide").eq(thisel.index());
        thisel.addClass("active").siblings("a").removeClass("active");
        currentb.addClass("active").siblings(".ot-slide").removeClass("active");
        thisel.parent().parent().css("height", currentb.attr("rel") + "px");
    }

    var sliderwidth = 0;


    jQuery(document).scroll(function () {
        var position = jQuery(window).scrollTop();

        if (position >= jQuery('.header #main-menu.thisisfixed').attr("rel")) {
            jQuery('.header #main-menu.thisisfixed').addClass("floatingmainmenu");
        } else {
            jQuery('.header #main-menu.thisisfixed').removeClass("floatingmainmenu");
        }
    });

    jQuery(window).resize(function () {
        var difference = (100 / sliderwidth * jQuery(".ot-slider").width()) / 100;
        jQuery(".ot-slider .ot-slides .ot-slide-overlay").css("zoom", difference);


        jQuery(".ot-slider .ot-slide").each(function () {
            var thisel = jQuery(this);

            jQuery(thisel).find("img").one('load', function () {
                thisel.attr("rel", thisel.height());
                jQuery(".ot-slider").each(function () {
                    var thisel = jQuery(this), curel = thisel.find(".ot-slides").children(".ot-slide").eq(0);
                    thisel.find(".ot-slider-thumbs").children("a").eq(0).addClass("active");
                    curel.addClass("active");
                    thisel.css("height", curel.attr("rel") + "px");
                });
            }).each(function () {
                if (this.complete) { jQuery(this).load(); }
            });
        });
    });

    jQuery(window).ready(function () {

        jQuery("body").append("<div class='menu-block'></div>");


        jQuery('.header #main-menu.thisisfixed').each(function () {
            var thiselement = jQuery(this);
            jQuery(this).children(".wrapper").wrap("<div class='subset'></div>");
            if (!thiselement.hasClass("thisisfloat")) {
                thiselement.attr("rel", thiselement.offset().top);
            }
        });

        jQuery("#main-menu .wrapper").prepend("<a href='#' class='menu-dropy'><i class='fa fa-align-justify'></i>&nbsp;&nbsp;Toggle menu</a>");

        jQuery(".menu-dropy").click(function () {
            var thisel = jQuery(this).siblings("ul");
            thisel.toggle();
            return false;
        });

        jQuery("#main-menu .wrapper > ul > li.overlay").hover(function () {
            jQuery(".boxed.active .header .header-topmenu").css("z-index", "0");
            jQuery(".menu-overlay").fadeIn(200);
        }).mouseleave(function () {
            jQuery(".menu-overlay").fadeOut(200);
            jQuery(".boxed.active .header .header-topmenu").css("z-index", "1002");
        });

        jQuery("a[href=#open-jumplist]").click(function () {
            jQuery(".ot-jumplist").addClass("active");
            return false;
        });

        jQuery("a[href=#close-jumplist]").click(function () {
            jQuery(".ot-jumplist").removeClass("active");
            return false;
        });

        jQuery(".ot-slider .ot-slide").each(function () {
            var difference = (100 / sliderwidth * jQuery(".ot-slider").width()) / 100,  thisel = jQuery(this);
            jQuery(".ot-slider .ot-slides .ot-slide-overlay").css("zoom", difference);


            // sliderwidth = thisel.width();
            sliderwidth = 1200;

            jQuery(thisel).find("img").one('load', function () {
                thisel.attr("rel", thisel.height());
                jQuery(".ot-slider").each(function () {
                    var thisel = jQuery(this), curel = thisel.find(".ot-slides").children(".ot-slide").eq(0);
                    thisel.find(".ot-slider-thumbs").children("a").eq(0).addClass("active");
                    curel.addClass("active");
                    thisel.css("height", curel.attr("rel") + "px");
                });
            }).each(function () {
                if (this.complete) { jQuery(this).load(); }
            });
        });



        jQuery(".ot-slider-thumbs a").click(function () {
            ot_Slider_move(jQuery(this));
            return false;
        });

        jQuery(".ot-slider .page-move.move-left").click(function () {
            var thisel = jQuery(this).parent(), nextind = thisel.find(".ot-slider-thumbs").children("a.active");
            if (nextind.prev().index() >= 0) {
                ot_Slider_move(nextind.prev());
            } else {
                ot_Slider_move(nextind.parent().children("a").last());
            }
            return false;
        });

        jQuery(".ot-slider .page-move.move-right").click(function () {
            var thisel = jQuery(this).parent(), nextind = thisel.find(".ot-slider-thumbs").children("a.active");
            if (nextind.next().index() >= 0) {
                ot_Slider_move(nextind.next());
            } else {
                ot_Slider_move(nextind.parent().children("a").eq(0));
            }
            return false;
        });


        jQuery("#main-menu .big-drop-2").each(function(){
            jQuery(this).find("ul.sub-menu > li > ul > li").eq(0).addClass("active");
        });

        jQuery("#main-menu .big-drop-2 > ul.sub-menu > li > ul > li > a").click(function () {
            var thisel = jQuery(this).parent(), thisindex = thisel.index();
            thisel.addClass("active").siblings("li").removeClass("active");
            jQuery("#main-menu .big-drop-2 > ul.sub-menu > li > ul.sub-menu").each(function () {
                var thisel = jQuery(this);
                thisel.css("height", thisel.find("li.active .menu-content-inner").height());
            });
            return false;
        });


        jQuery("#main-menu .big-drop-2").hover(function () {
            jQuery("#main-menu .big-drop-2 > ul.sub-menu > li > ul.sub-menu").each(function () {
                var thisel = jQuery(this);
                thisel.css("height", thisel.find("li.active .menu-content-inner").height());
            });
        });


        // Alert box close
        jQuery('a[href="#close-alert"]').click(function () {
            jQuery(this).parent().animate({
                opacity: 0,
                padding: "0px 13px",
                margin: "0px",
                height: "0px"
            }, 300, function () {
                // Animation complete.
            });
            return false;
        });

        // Accordion blocks
        jQuery(".accordion > div > a").click(function () {
            var thisel = jQuery(this).parent();
            if (thisel.hasClass("active")) {
                thisel.removeClass("active").children("div").animate({
                    "height": "toggle",
                    "opacity": "toggle",
                    "padding-top": "toggle"
                }, 300);
                return false;
            }
            // thisel.siblings("div").removeClass("active");
            thisel.siblings("div").each(function () {
                var tz = jQuery(this);
                if (tz.hasClass("active")) {
                    tz.removeClass("active").children("div").animate({
                        "height": "toggle",
                        "opacity": "toggle",
                        "padding-top": "toggle"
                    }, 300);
                }
            });
            // thisel.addClass("active");
            thisel.addClass("active").children("div").animate({
                "height": "toggle",
                "opacity": "toggle",
                "padding-top": "toggle"
            }, 300);
            return false;
        });


        // Tabbed blocks
        jQuery(".short-tabs").each(function () {
            var thisel = jQuery(this);
            thisel.children("div").eq(0).addClass("active");
            thisel.children("ul").children("li").eq(0).addClass("active");
        });

        jQuery(".short-tabs > ul > li a").click(function () {
            var thisel = jQuery(this).parent();
            thisel.siblings(".active").removeClass("active");
            thisel.addClass("active");
            thisel.parent().siblings("div.active").removeClass("active");
            thisel.parent().siblings("div").eq(thisel.index()).addClass("active");
            return false;
        });

        jQuery(".lightbox").click(function () {
            jQuery(".lightbox").css('overflow', 'hidden');
            jQuery("body").css('overflow', 'auto');
            jQuery(".lightbox .lightcontent").fadeOut('fast');
            jQuery(".lightbox").fadeOut('slow');
        }).children().click(function (e) {
            return false;
        });



        jQuery("a[href='#font-size-up']").click(function () {
            var cursize = jQuery('.f-size-number').html();
            if (parseInt(cursize) < 24) {
                jQuery('.f-size-number').html(parseInt(cursize) + 2);
                jQuery('.main-article p').css("font-size", (parseInt(cursize) + 2) + "px");
            }
            return false;
        });

        jQuery("a[href='#font-size-down']").click(function () {
            var cursize = jQuery('.f-size-number').html();
            if (parseInt(cursize) > 16) {
                jQuery('.f-size-number').html(parseInt(cursize) - 2);
                jQuery('.main-article p').css("font-size", (parseInt(cursize) - 2) + "px");
            }
            return false;
        });


        // Breaking News Scroller
        jQuery(".breaking-news .breaking-block").each(function () {
            var thisitem = jQuery(this);
            thisitem.find("ul li").css("width", thisitem.width() + "px");
        });

        jQuery(".breaking-controls a").click(function () {
            var thisitem = jQuery(this), itemul = thisitem.parent().parent().find(".breaking-block ul"), items = itemul.find("li"), sega = (items.size() - 1) * (items.width() + parseInt(items.css("margin-right")));
            if (thisitem.hasClass("breaking-arrow-left")) {
                if (0 >= Math.abs(parseInt(itemul.css("margin-left")))) {
                    itemul.css("margin-left", (sega * (-1)) + "px");
                } else {
                    itemul.css("margin-left", (parseInt(itemul.css("margin-left")) + (items.width() + parseInt(items.css("margin-right")))) + "px");
                }
            } else {
                if (sega <= Math.abs(parseInt(itemul.css("margin-left")))) {
                    itemul.css("margin-left", "0px");
                } else {
                    itemul.css("margin-left", (parseInt(itemul.css("margin-left")) + (items.width() + parseInt(items.css("margin-right"))) * (-1)) + "px");
                }
            }
            return false;
        });

        jQuery(".breaking-news").mouseenter(function () {
            var thisindex = jQuery(this).attr("rel");
            clearTimeout(elementsActive[thisindex]);
        }).mouseleave(function () {
            var thisindex = jQuery(this).attr("rel");
            elementsActive[thisindex] = false;
        });

        start();
        
        
		jQuery('.ot-star-rating').each( function(i){
			var bottom_of_object = jQuery(this).offset().top + jQuery(this).outerHeight(), bottom_of_window = jQuery(window).scrollTop() + jQuery(window).height();

			if( bottom_of_window <= bottom_of_object ){
                var thisel = jQuery(this).children("span");
                thisel.addClass("setforanimate").attr("rel", thisel.css("width")).css("width", "0px");
			}
		});

		jQuery(window).scroll( function(){
			jQuery('.ot-star-rating').each( function(i){
				var bottom_of_object = jQuery(this).offset().top + jQuery(this).outerHeight(), bottom_of_window = jQuery(window).scrollTop() + jQuery(window).height();

				if( bottom_of_window > bottom_of_object ){
                    var thisel = jQuery(this).children("span.setforanimate");
					thisel.removeClass("setforanimate").css("display", "block").animate( {'width':thisel.attr("rel")}, 500 );
				}
			});
		});

    });

})(jQuery);


function start() {
    var z = 0;
    jQuery('.breaking-block ul').each(function () {
        var thisitem = jQuery(this), thisindex = z;
        z = z + 1;
        if (thisitem.find("li").size() > 0) {

            if (!breakingStart) { return false; }
            var theBreakingMargin = parseInt(thisitem.find("li").css("margin-right")), theBreakingWidth = parseInt(thisitem.parent().css("width"));
            theCount[thisindex] = ((Math.ceil(thisitem.find("li").size()) / 2) * (theBreakingWidth + theBreakingMargin));

            if (elementsToClone[thisindex]) {
                jQuery(this).parent().parent().addClass("isscrolling");
                jQuery('.breaking-block').eq(thisindex).parent().attr("rel", thisindex);
                thisitem.find("li").clone().appendTo(this);

                elementsToClone[thisindex] = false;
            }
            var theNumber = theCount[thisindex] + breakingOffset[thisindex];

            if (Math.abs(theNumber) <= (Math.abs(breakingScroll[thisindex]))) {
                cloneBreakingLine(thisindex);
            }

            if (!elementsActive[thisindex]) {
                elementsActive[thisindex] = setInterval(function () {
                    beginScrolling(thisitem, thisindex);
                }, breakingSpeed);
            }
        }
    });

    setTimeout("start()", breakingSpeed);
}

function beginScrolling(thisitem, thisindex) {
    breakingScroll[thisindex] = breakingScroll[thisindex] - 1;
    thisitem.css("left", breakingScroll[thisindex] + 'px');
}

function cloneBreakingLine(thisindex) {
    breakingScroll[thisindex] = 0;
    jQuery('.breaking-block').eq(thisindex).find('ul').css("left", "0px");
}






function lightboxclose() {
    jQuery(".lightbox").css('overflow', 'hidden');
    jQuery(".lightbox .lightcontent").fadeOut('fast');
    jQuery(".lightbox").fadeOut('slow');
    jQuery("body").css('overflow', 'auto');
}