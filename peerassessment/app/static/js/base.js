function showNotification() {
	console.log("Show Notification");
	$("#notification").addClass("open");

}

$('html').click(function() {
	$("#notification").removeClass("open");
});

$('#notification').click(function(event){
    event.stopPropagation();
});