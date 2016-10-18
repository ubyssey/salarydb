
$(function(){

    $(".dropdown .dropdown-link").click(function(e){
        e.preventDefault();
        var par = $(this).parent();
        if(par.hasClass("chosen-with-drop")){
            par.removeClass("chosen-with-drop");
        } else {
            par.addClass("chosen-with-drop");
        }
    });

    $(".search-filter").show();
    $(".search-filter").each(function(){
        var val = $(this).data("val");
        if (val)
            $(this).val(val);
    });

    $(".search-filter").chosen({disable_search_threshold: 10, allow_single_deselect: true}).change(function(){
        var filter = $(this).data("filter");
        var value = $(this).val();
        var parsed = queryString.parse(location.search);
        delete parsed.pg;
        if(value){
            parsed[filter] = value;
        } else {
            delete parsed[filter];
        }
        window.location.href = BASE_URL + "search/?" + queryString.stringify(parsed);
    });


    $(".search-page #search-form").submit(function(e){
        e.preventDefault();
        var parsed = queryString.parse(location.search);
        parsed.q = $("#search-field").val();
        delete parsed.pg;
        location.search = queryString.stringify(parsed);
    });

    $( "#search-field" ).autocomplete({
            source: function( request, response ) {
            $.get(BASE_URL + 'api/search/', { q: request.term }, function(data){
            response(data);
        });
        },
        focus: function (event, ui) {
            event.preventDefault();
            $(this).val(ui.item.name);
        },
        minLength: 3,
        appendTo: '.search-dropdown',
        position: { my: "left top-5", at: "left bottom", collision: "none" },
        select: function( event, ui ) {
            $(this).parent().submit();
        },
        open: function() {
            $( this ).addClass("no-bottom-corner");
        },
        close: function() {
            $( this ).removeClass("no-bottom-corner");
        }
    }).autocomplete( "instance" )._renderItem = function( ul, item ) {
        return $( "<li>" )
            .attr( "data-value", item.name )
            .append(
                $("<a>")
                    .attr("href", BASE_URL+"employee/"+item.url)
                    .append(item.name)
                )
            .appendTo( ul );
        }
});
