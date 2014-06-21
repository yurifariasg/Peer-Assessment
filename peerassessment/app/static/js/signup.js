function IsEmail(email) {
  var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  return regex.test(email);
}

function signup() {
	console.log("Button Pressed");

	var firstname = $("#name").val();
	var lastname = $("#lastname").val();
	var email = $("#email").val();
	var password = $("#password").val();
	var confirmPassword = $("#confirmPassword").val();	

	if(!firstname.trim() || !lastname.trim()) {
		$('.alert').show();
		$("#msg").text("Nome/sobrenome não podem estar vazio");
		return;
	 }

	 if (!IsEmail(email)) {
	 	$('.alert').show();
		$("#msg").text("Email inválido");
		return;
	 }

	 if (password != confirmPassword) {
	 	console.log("ERRO NA SENHA")
	 	$('.alert').show();
		$("#msg").text("Erro na confirmação da senha");
		return;
	 }

	var content = JSON.stringify({ 
		"firstname" : firstname,
		"lastname" : lastname,
		"password" : password,
		"email" : email,
		"type" : "student"
	});

	$.post("/register", content,
	 function( data, txtStatus, xhr ) {
		// Sucessful!
		window.location.href = "/";
	})
	.fail(function(data, txtStatus, xhr) {
		$('.alert').show();
		console.log("fail: " + data.responseText);
		json_body = JSON.parse(data.responseText);
		$("#msg").text(json_body.error);	
	});

}

