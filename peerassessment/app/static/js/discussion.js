
// This is the JS for the Discussion Page

$('textarea').css('overflow', 'hidden').autosize(
  {"append" : "",
  "callback": function() {
    var height = $(this).height()
    $(this).parent().find(".btn").height(height);
    }
  }
);

$('.btn-send').click(function() {
    var parent = $(this).parent().parent();
    var message = parent.find("textarea").val();
    var btn = $(this);
    btn.prop('disabled', true);
    var animation = $("#loading-template").clone();
    btn.empty();
    btn.append(animation);
    animation.show();

    content = {
        "assignment_id" : $("#assignment").data('id'),
        "messages" : [{
            "peer" : parent.data('peer'),
            "criteria" : parent.data('criteria'),
            "message" : message
        }]
    };

    $.post("/assignment/message", JSON.stringify(content),
     function( data, txtStatus, xhr ) {
        // Sucessful!
        var clonedBubble = $("#mine-bubble-template").clone();
        clonedBubble.insertBefore(parent);
        clonedBubble.show();
        clonedBubble.html(message.replace(/\n/g, "</br>"));
        parent.find("textarea").val("").trigger('autosize.resize');

    })
    .fail(function(data, txtStatus, xhr) {
        console.log("fail: " + data.responseText);
    })
    .always(function() {
        btn.empty()
        var icon = $("#send-icon-template").clone();
        btn.append(icon);
        icon.show();
        btn.prop('disabled', false);
    });


    // IF OK

    // var clonedBubble = $("#mine-bubble-template").clone();
    // clonedBubble.insertBefore(parent);
    // clonedBubble.show();
    // clonedBubble.html(message.replace(/\n/g, "</br>"));
    // parent.find("textarea").val("").trigger('autosize.resize');

    // $(this).empty()
    // var icon = $("#send-icon-template").clone();
    // $(this).append(icon);
    // icon.show();
    // $(this).prop('disabled', false);
});
