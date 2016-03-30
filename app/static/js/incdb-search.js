$(document).ready(function() {
    $("#search_movie").autocomplete({

        source: function(request, response) {
            $.getJSON($SCRIPT_ROOT + "/_search_movie", 
                { movie: request.movie }, 
                response);
        },
        minLength: 2,
        messages: {
            noResults: '',
            results: function() {}
        }

    });
});