(function($){
$(document).on("keyup","input", function(){
    if ($(this)[0].id !="id_establecimientos_input") return
    var querystring = $("#id_establecimientos_input").val();
    if (querystring && querystring.length >= 3) {
        $.ajax ({
            type: "GET",
            url: "/establecimientos/get_json_establecimientos/"+querystring+"/",
            cache: false,
            success: function(json) {
                if (json) {
                    var list_from = $("#id_establecimientos_from option").map(function() {
                        return parseInt($(this).val());
                    });
                    var list_to = $("#id_establecimientos_to option").map(function() {
                        return parseInt($(this).val());
                    });
                    for (var pid in json) {
                        if ($.inArray(json[pid].id, list_from) == -1 && $.inArray(json[pid].id, list_to) == -1) {
                            $("#id_establecimientos_from").prepend("<option value='"+json[pid].id+"'>"+json[pid].name+"</option>");
                        }
                    }
                    SelectBox.init('id_establecimientos_from');
                    SelectBox.init('id_establecimientos_to');
                }
            }
        });
    }
})
}(django.jQuery));