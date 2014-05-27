
function login() {
	var email = $("#email_field").val();
	var password = $("#password_field").val();

	var content = JSON.stringify({ "email" : email, "password" : password });

	$.post("login", content,
	 function( data ) {
		// Sucessful!
		window.location.href = "http://localhost:8000/student/";
	})
	.fail(function(data, txtStatus, xhr) {
		console.log("fail: " + data.responseText);
	});
}