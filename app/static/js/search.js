$(document).ready(function() {
    $("#search_movie").autocomplete({

        source: function(request, response) {
            $.getJSON($SCRIPT_ROOT + "/_search_movie", 
                { term: request.term }, 
                response);
        },
        minLength: 2,
        messages: {
            noResults: '',
            results: function() {}
        }

    });
});