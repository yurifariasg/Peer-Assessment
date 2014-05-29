
function login() {
	var email = $("#email_field").val();
	var password = $("#password_field").val();

	var content = JSON.stringify({ "email" : email, "password" : password });

	$.post("login", content,
	 function( data, txtStatus, xhr ) {
		// Sucessful!
		window.location = JSON.parse(data).url;
	})
	.fail(function(data, txtStatus, xhr) {
		console.log("fail: " + data.responseText);
	});
}