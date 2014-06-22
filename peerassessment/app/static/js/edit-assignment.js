
// This is the JS for the Edit Assignment page

$("#addCriteria").click(function(event) {
    newCriteria = $("#template_criteria").clone()
    $(".criterias").append(newCriteria)
    newCriteria.show();

});

$("#removeCriteria").click(function(event) {
    if ($(".criterias .criteria").length > 1) {
        $(".criterias .criteria").last().remove();
    }
});


// This will be removed when we have Issue #30
var getStageString = function(stage) {
    if (stage == "Submission") {
        return "Submissão";
    } else if (stage == "Discussion") {
        return "Discussão";
    } else if (stage == "Grading") {
        return "Nota";
    } else {
        return "Fechado";
    }
};

var onChangeDate = function(e, dateType) {
    var new_stage = checkStageBasedOnPickers();
    warning_container = $("#warning-container");
    if (new_stage != currentStage) {
        warning_container.html(
            "A atividade mudará para a fase <strong>" + getStageString(new_stage) + "</strong>"
        );
        warning_container.show();
    } else {
        warning_container.hide();
    }

    setMinAndMaxDates();
};

var setMinAndMaxDates = function() {
    var submissionPicker = $('#submission-picker').data("DateTimePicker");
    var discussionPicker = $('#discussion-picker').data("DateTimePicker");
    var gradingPicker = $('#grading-picker').data("DateTimePicker");

    var submissionDate = submissionPicker.getDate();
    var discussionDate = discussionPicker.getDate();
    var gradingDate = gradingPicker.getDate();

    submissionPicker.setMaxDate(discussionDate);
    discussionPicker.setMinDate(submissionDate);
    discussionPicker.setMaxDate(gradingDate);
    gradingPicker.setMinDate(discussionDate);
}

var dateOptions = {
    language: 'pt-BR',
    useSeconds: false,
    format: "DD/MM/YYYY HH:mm"
}

var checkStageBasedOnPickers = function() {
    var date_submission = $('#submission-picker').data("DateTimePicker").getDate();
    var date_discussion = $('#discussion-picker').data("DateTimePicker").getDate();
    var date_grading = $('#grading-picker').data("DateTimePicker").getDate();
    var now = moment();

    if (date_submission < now) {
        if (date_discussion < now) {
            if (date_grading < now) {
                return "Closed";
            } else {
                return "Grading";
            }
        } else {
            return "Discussion";
        }
    } else {
        return "Submission";
    }
};


$('#submission-picker').datetimepicker(dateOptions).on("dp.change", function(e) {
    onChangeDate(e, 'submission')
});
$('#discussion-picker').datetimepicker(dateOptions).on("dp.change", function(e) {
    onChangeDate(e, 'discussion')
});
$('#grading-picker').datetimepicker(dateOptions).on("dp.change", function(e) {
    onChangeDate(e, 'grading')
});

setMinAndMaxDates();

$("#createAssignment").click(function(event) {

    var name = $("input[type=name],select").val();

    var dateFormat = 'YYYY-MM-DDTHH:mm:SS';

    var submission_end_date = $("#submission-picker").data("DateTimePicker").getDate();
    var discussion_end_date = $("#discussion-picker").data("DateTimePicker").getDate();
    var grading_end_date = $("#grading-picker").data("DateTimePicker").getDate();
    var id = $("#assignment").data('id');

    var assignment = {
        "id" : id,
        "name" : name,
        "submission_end_date" : submission_end_date.format(dateFormat),
        "discussion_end_date" : discussion_end_date.format(dateFormat),
        "grading_end_date" : grading_end_date.format(dateFormat),
        "criterias" : []
    };

    $(".criterias .criteria").each(function() {

        var description = $(this).find("input[type=description],select").val();
        var weight = $(this).find("input[type=weight],select").val();
        var id = $(this).data("id");

        assignment["criterias"].push({"id" : id, "name" : description, "weight" : weight});

    });

    var content = JSON.stringify(assignment);

    $.post("/assignment/edit", content,
     function( data, txtStatus, xhr ) {
        // Sucessful!
        window.location.href = "/";
    })
    .fail(function(data, txtStatus, xhr) {
        console.log("fail: " + data.responseText);
    });
});

// Let's keep here our current stage
// This will run once, so we will get the stage of the assignment
// Since the pickers will point exactly to its end dates.
var currentStage = checkStageBasedOnPickers();
