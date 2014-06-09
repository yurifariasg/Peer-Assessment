
$("#addCriteria").click(function(event) {
    console.log("Add");
    newCriteria = $("#template_criteria").clone()
    $(".criterias").append(newCriteria)
    newCriteria.show();

});

$("#removeCriteria").click(function(event) {
    console.log("Remove");
    if ($(".criterias .criteria").length > 1) {
        $(".criterias .criteria").last().remove();
    }
});

$("#createAssignment").click(function(event) {

    var name = $("input[type=name],select").val();

    var dateFormat = 'YYYY-MM-DDTHH:MM:SS';

    var submission_end_date = $("#submission-picker").data("DateTimePicker").getDate();
    var discussion_end_date = $("#discussion-picker").data("DateTimePicker").getDate();
    var grading_end_date = $("#grading-picker").data("DateTimePicker").getDate();

    var assignment = {
        "name" : name,
        "submission_end_date" : submission_end_date.format(dateFormat),
        "discussion_end_date" : discussion_end_date.format(dateFormat),
        "grading_end_date" : grading_end_date.format(dateFormat),
        "criterias" : []
    };

    $(".criterias .criteria").each(function() {

        var description = $(this).find("input[type=description],select").val();
        var weight = $(this).find("input[type=weight],select").val();

        assignment["criterias"].push({"name" : description, "weight" : weight});

    });

    var content = JSON.stringify(assignment);

    console.log(content);

    $.post("/assignment/create", content,
     function( data, txtStatus, xhr ) {
        // Sucessful!
        // window.location = JSON.parse(data).url;
        window.location.href = "/";
    })
    .fail(function(data, txtStatus, xhr) {
        console.log("fail: " + data.responseText);
    });


});

var yesterday = new Date();
yesterday.setDate(yesterday.getDate()-1);

var dateOptions = {
    language: 'pt-BR',
    useSeconds: false,
    minDate: yesterday
}

$('#submission-picker').datetimepicker(dateOptions);
$('#discussion-picker').datetimepicker(dateOptions);
$('#grading-picker').datetimepicker(dateOptions);
