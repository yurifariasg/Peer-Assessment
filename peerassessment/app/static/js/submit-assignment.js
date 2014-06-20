$("#submitAssignment").click(function(event) {

	var url = $("#linkassignment").val();
	var id = $("#assignmentid").data("id");

	var assignment = {
        "url" : url,
        "assignment_id" : id
    };
	
	var content = JSON.stringify(assignment);

	$.post("/assignment/submit", content,
     function( data, txtStatus, xhr ) {
        // Sucessful!
        // window.location = JSON.parse(data).url;
        window.location.href = "/";
    })
    .fail(function(data, txtStatus, xhr) {
        console.log("fail: " + data.responseText);
    });
});