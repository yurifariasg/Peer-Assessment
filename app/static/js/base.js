function showNotification() {
	console.log("Show Notification");
	$("#notification").addClass("open");
}

function showSettings() {
	console.log("Show Settings");
	$("#settings").addClass("open");
}

function logout() {
	$.get("/logout",
	function( data, txtStatus, xhr ) {
		// Sucessful!
		window.location = JSON.parse(data).url;
	})
	.fail(function(data, txtStatus, xhr) {
		console.log("Failed to Logout: " + data);
	});
}

$('html').click(function() {
	$("#notification").removeClass("open");
	$("#settings").removeClass("open");
});

$('#notification').click(function(event){
	$("#settings").removeClass("open");
    event.stopPropagation();
});

$('#settings').click(function(event){
	$("#notification").removeClass("open");
	event.stopPropagation();
});
