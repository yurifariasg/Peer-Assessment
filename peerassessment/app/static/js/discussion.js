
// This is the JS for the Discussion Page

// Below is the minified version of JQuery-Color
// A JQuery plugin to animate colors
(function(d){d.each(["backgroundColor","borderBottomColor","borderLeftColor","borderRightColor","borderTopColor","color","outlineColor"],function(f,e){d.fx.step[e]=function(g){if(!g.colorInit){g.start=c(g.elem,e);g.end=b(g.end);g.colorInit=true}g.elem.style[e]="rgb("+[Math.max(Math.min(parseInt((g.pos*(g.end[0]-g.start[0]))+g.start[0]),255),0),Math.max(Math.min(parseInt((g.pos*(g.end[1]-g.start[1]))+g.start[1]),255),0),Math.max(Math.min(parseInt((g.pos*(g.end[2]-g.start[2]))+g.start[2]),255),0)].join(",")+")"}});function b(f){var e;if(f&&f.constructor==Array&&f.length==3){return f}if(e=/rgb\(\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*\)/.exec(f)){return[parseInt(e[1]),parseInt(e[2]),parseInt(e[3])]}if(e=/rgb\(\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*\)/.exec(f)){return[parseFloat(e[1])*2.55,parseFloat(e[2])*2.55,parseFloat(e[3])*2.55]}if(e=/#([a-fA-F0-9]{2})([a-fA-F0-9]{2})([a-fA-F0-9]{2})/.exec(f)){return[parseInt(e[1],16),parseInt(e[2],16),parseInt(e[3],16)]}if(e=/#([a-fA-F0-9])([a-fA-F0-9])([a-fA-F0-9])/.exec(f)){return[parseInt(e[1]+e[1],16),parseInt(e[2]+e[2],16),parseInt(e[3]+e[3],16)]}if(e=/rgba\(0, 0, 0, 0\)/.exec(f)){return a.transparent}return a[d.trim(f).toLowerCase()]}function c(g,e){var f;do{f=d.css(g,e);if(f!=""&&f!="transparent"||d.nodeName(g,"body")){break}e="backgroundColor"}while(g=g.parentNode);return b(f)}var a={aqua:[0,255,255],azure:[240,255,255],beige:[245,245,220],black:[0,0,0],blue:[0,0,255],brown:[165,42,42],cyan:[0,255,255],darkblue:[0,0,139],darkcyan:[0,139,139],darkgrey:[169,169,169],darkgreen:[0,100,0],darkkhaki:[189,183,107],darkmagenta:[139,0,139],darkolivegreen:[85,107,47],darkorange:[255,140,0],darkorchid:[153,50,204],darkred:[139,0,0],darksalmon:[233,150,122],darkviolet:[148,0,211],fuchsia:[255,0,255],gold:[255,215,0],green:[0,128,0],indigo:[75,0,130],khaki:[240,230,140],lightblue:[173,216,230],lightcyan:[224,255,255],lightgreen:[144,238,144],lightgrey:[211,211,211],lightpink:[255,182,193],lightyellow:[255,255,224],lime:[0,255,0],magenta:[255,0,255],maroon:[128,0,0],navy:[0,0,128],olive:[128,128,0],orange:[255,165,0],pink:[255,192,203],purple:[128,0,128],violet:[128,0,128],red:[255,0,0],silver:[192,192,192],white:[255,255,255],yellow:[255,255,0],transparent:[255,255,255]}})(jQuery);

// Discussion and Grade page Functions

$('textarea').css('overflow', 'hidden').autosize(
  {"append" : "",
  "callback": function() {
    var height = $(this).height()
    $(this).parent().find(".btn").height(height);
    }
  }
);

$("input[type=grade]").keydown(function () {
    var field = $(this)
    setTimeout(function () {
        var val = field.val()
        var floatVal = parseFloat(val);
        if (val.length == 0 || isNaN(floatVal) || floatVal > 10 || floatVal < 0) {
            field.parent().find(".form-control-feedback").show();
            field.parent().addClass("has-error");
            return;
        }
        field.parent().find(".form-control-feedback").hide();
        field.parent().removeClass("has-error");
    }, 1);
});


var changeButtonColor = function(btn, color) {
    btn.animate({
        backgroundColor: color
    }, 1000, function() {
        setTimeout(function() {
            btn.animate({backgroundColor: 'rgb(255, 255, 255)'});
        }, 1000);
    });
}

$('.btn-save-grade').click(function() {
    var btn = $(this);
    var component = $(this).parent().parent();
    var grade = component.find('input[type=grade]').val();
    var criteria = component.data('criteria');
    var peer = component.data('peer');
    var assignment_id = $("#assignment").data('id');

    var content = { 'assignment' : assignment_id,
        'grades' : [
            { 'peer' : peer, 'grades' : [ { 'criteria' : criteria, 'grade' : grade } ] }
        ]
    };

    var animation = $("#loading-template").clone();
    var oldContent = btn.html();
    btn.empty();
    btn.append(animation);
    animation.show();
    btn.prop('disabled', true);

    console.log(content);

    $.post("/assignment/grade", JSON.stringify(content),
     function( data, txtStatus, xhr ) {
        // Sucessful!
        changeButtonColor(btn, 'rgb(152, 255, 189)');
    })
    .fail(function(data, txtStatus, xhr) {
        console.log("fail: " + data.responseText);
        changeButtonColor(btn, 'rgb(255, 165, 165)');
    })
    .always(function() {
        btn.empty()
        btn.html(oldContent);
        btn.prop('disabled', false);
    });
});

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
});
