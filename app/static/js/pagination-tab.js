$(document).ready(function() {
    var foo = getParameterByName('page');
    if (foo != null) {
        var tablink = $('.nav-tabs a[href="#components"]');
        if(tablink != null) {
            $('.nav-tabs a[href="#components"]').tab('show');
        }
    }
});

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}