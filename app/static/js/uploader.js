// Constants
var UPLOAD_URL = "/upload";
var NEXT_URL   = "/collection/";

// List of pending files to handle when the Upload button is finally clicked.
var PENDING_FILES  = [];

$(document).ready(function() {

    var input = $("#file-picker");
    var labelVal = $("#file-label").innerHTML;

    // Set up the handler for the file input box.
    input.on("change", function(e) {

        var fileName = '';

            if( this.files && this.files.length > 1 )
                fileName = ( this.getAttribute( 'data-multiple-caption' ) || '' ).replace( '{count}', this.files.length );
            else
                fileName = e.target.value.split( '\\' ).pop();

            if(fileName) {
                var re = /(\.zip|\.tar.gz)$/i;
                if(!re.exec(fileName))
                    alert("File extension not supported");
                else
                    $('#file-span').text(fileName);
                    handleFiles(this.files);
            } else {
                $("#file-label").innerHTML = labelVal;
            }

    });

    // Handle the submit button.
    $("#upload-button").on("click", function(e) {
        // If the user has JS disabled, none of this code is running but the
        // file multi-upload input box should still work. In this case they'll
        // just POST to the upload endpoint directly. However, with JS we'll do
        // the POST using ajax and then redirect them ourself when done.
        e.preventDefault();
        if (PENDING_FILES.length>0) {
            doUpload();
        } else {
            alert("Please select a file to upload");
        }
        
    })

});


function doUpload() {

    $("#progress").show();
    var $progressBar   = $("#progress-bar");

    // Gray out the form.
    $("#upload-form :input").attr("disabled", "disabled");

    // Initialize the progress bar.
    $progressBar.css({"width": "0%"});

    // Collect the form data.
    fd = collectFormData();

    // Attach the files.
    for (var i = 0, ie = PENDING_FILES.length; i < ie; i++) {
        // Collect the other form data.
        fd.append("file", PENDING_FILES[i]);
    }

    // Inform the back-end that we're doing this over ajax.
    fd.append("__ajax", "true");

    var xhr = $.ajax({
        xhr: function() {
            var xhrobj = $.ajaxSettings.xhr();
            if (xhrobj.upload) {
                xhrobj.upload.addEventListener("progress", function(event) {
                    var percent = 0;
                    var position = event.loaded || event.position;
                    var total    = event.total;
                    if (event.lengthComputable) {
                        percent = Math.ceil(position / total * 100);
                    }

                    // Set the progress bar.
                    $progressBar.css({"width": percent + "%"});
                    $progressBar.text(percent + "%");
                }, false)
            }
            return xhrobj;
        },
        url:  $('#upload-form').attr('action'),
        method: "POST",
        contentType: false,
        processData: false,
        cache: false,
        data: fd,
        success: function(data) {
            $progressBar.css({"width": "100%"});
            data = JSON.parse(data);

            // How'd it go?
            if (data.status === "error") {
                // Uh-oh.
                window.alert(data.msg);
                $("#upload-form :input").removeAttr("disabled");
                return;
            }
            else {
                // Ok! Get the UUID.
                var uuid = data.msg;
                window.location = NEXT_URL + uuid;
            }
        },
    });
}


function collectFormData() {

    // Go through all the form fields and collect their names/values.
    var fd = new FormData();

    $("#upload-form :input").each(function() {

        var $this = $(this);
        var name  = $this.attr("name");
        var type  = $this.attr("type") || "";
        var value = $this.val();

        // Skip the file upload box for now.
        if (type === "file") {
            return;
        }

        fd.append(name, value);
    });

    return fd;
}


function handleFiles(files) {
    // Add them to the pending files list.
    for (var i = 0, ie = files.length; i < ie; i++) {
        PENDING_FILES.push(files[i]);
        console.log(PENDING_FILES[i]);
    }
}