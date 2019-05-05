/* 
$(".fancybox").fancybox({
	padding: 0
});
 
$(".ajax-link").fancybox({
	padding: 0,
	type: "ajax"
});
 
$(".video-link").fancybox({
	padding: 0,
	type: "iframe"
});
*/
$(".ajax-link").click(function(){
	var href = $(this).attr("href");
	$.ajax({
		url: href,
		success: function(data){
			
			 showAjaxPage(data);
		}
	});
	return false;
});
$("#online").click(function(){
	$("#kefu-prompt").addClass("active");
	return false;
});
 
$(".prompt-overlay").click(function(){
	$(".prompt").removeClass("active");
});

function showAjaxPage(content){
	$("#ajax-page-content").html(content);
	var scrollTop = $(window).scrollTop();
	$("body").addClass("ajax-page-active");
	$("#wrap").css("top", -scrollTop);
	$(window).scrollTop(0);
}
$("#ajax-page-overlay").click(function(){
	 
	$("body").removeClass("ajax-page-active");
	 
	$(window).scrollTop( Math.abs(parseInt($("#wrap").css("top"))) );
	$("#wrap").css("top", 0);
});
if(window.innerWidth > 900){
	$(".section-home-slide").height( (window.innerHeight - 120) * 0.8 );
	
	$(".page-cover").height((window.innerHeight - 120)*0.5);
	$(".page-caption").height((window.innerHeight - 120)*0.5);
	
}else{
	$(".section-home-slide").height( window.innerHeight * 0.4);
}

$("#home-slide").slidesjs({
	width: $("#home-slide").width(),
	height: $("#home-slide").height(),
	play: {
		auto: true,
	}
});
$("#home-slide").css("overflow","visible");
$("#home-slide .slidesjs-previous").html("&#xe600;");
$("#home-slide .slidesjs-next").html("&#xe601;");
$("#home-slide .slidesjs-navigation").addClass("icon-font");

$(".slidesjs-navigation").css("top", ( $("#home-slide").height() - 130)  / 2);

$(".mobile-menu").click(function(){
	$(".menu").addClass("active");
});



$(document).scroll(function(){
 
	var scrollTop = $(document).scrollTop();
	if( scrollTop > 100){
		$("#header").addClass("scrolled");
		$(".page-cover").addClass("scrolled");
	}else{
		$("#header").removeClass("scrolled");
		$(".page-cover").removeClass("scrolled");
	}
	
	/*
	if( scrollTop > 3*window.innerHeight){
		$("body").addClass("scroll-bottom");
	}else{
		$("body").removeClass("scroll-bottom");
	}
	*/
	
	if(scrollTop < 200){
		$("body").removeClass("scroll-bottom");
		$("body").removeClass("scroll-cy");
	}else if(scrollTop >= 200 && scrollTop < 2*window.innerHeight){
		$("body").addClass("scroll-cy");
		$("body").removeClass("scroll-bottom");
	}else{
		$("body").addClass("scroll-bottom");
		$("body").removeClass("scroll-cy");
	}
});

$(".lang").click(function(){
	$url = window.location.href.split("?")[0];
	if($(this).hasClass("chinese-only")){
		window.location = $url + "?lang=en";
	}else{
		window.location = $url + "?lang=cn";
	}
});

$(".page-fullscreen").height(window.innerHeight - 50);


$(".work-wrap").each(function(){
	 
	var workItem = $(this);
	if(workItem.hasClass("no-equal")){
		return false;
	}
	var col = 2;
	if(workItem.hasClass("col-3")){
		col = 3;
	} else if(workItem.hasClass("col-4")){
		col = 4;
	
	} else if(workItem.hasClass("col-5")){
		col = 5;
	}
	
	var workInfo = workItem.find(".work-info-inner");
	
	var count = 0;
	var heightArray = {};
	 
	workInfo.each(function(){
		var thisInfo = $(this);
		var height = thisInfo.height();
		var index = Math.floor( count / col );
		
		count ++;
		if(heightArray){
			
			if(heightArray[index]){
				if(height > heightArray[index]){
					heightArray[index] = height ;
				}
			}else{
				heightArray[index] = height ;
			}
		}else{
			heightArray[index] = height ;
		}
		 
	});
	var count = 0;
	workInfo.each(function(){
		var thisInfo = $(this);
		
		var index = Math.floor( count / col );
		
		count ++;
		thisInfo.height(heightArray[index]);
	});
	
});


$(".news-wrap .work-info").each(function(){
	 
	 
});

$(".para-wrap .work-info").each(function(){
	var node = $(this);
	node.height(node.parents(".work-item").find(".work-image").height()); 
	node.parents(".work-item").
	find(".work-image img").get(0).onload = function(){
	
		 node.height(node.parents(".work-item").find(".work-image").height());
	}
	 
});





