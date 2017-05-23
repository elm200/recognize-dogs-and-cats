// Thanks to http://www.it-view.net/drag-and-drop-file-upload-jquery-178.html
function sendFilesToServer(files) {
  var formData = new FormData();
  formData.append('upfile', files[0]);
  var jqXHR = $.ajax({
    url: "/upload",
    type: "POST",
    contentType: false,
    processData: false,
    cache: false,
    data: formData,
    success: function(data) {
      $("#status1").append("File upload Done<br>");
    }
  });
}

$(document).ready(function() {
  var droparea = $("#droparea");

  droparea.on('dragenter', function(e) {
    e.stopPropagation();
    e.preventDefault();
    $(this).css('border', '2px solid #0B85A1');
  });

  droparea.on('dragover', function(e) {
    e.stopPropagation();
    e.preventDefault();
  });

  droparea.on('drop', function(e) {
    $(this).css('border', '2px dotted #0B85A1');
    e.preventDefault();
    var files = e.originalEvent.dataTransfer.files;
    console.log(files.length);
    sendFilesToServer(files);
  });

  $(document).on('dragenter', function(e) {
    e.stopPropagation();
    e.preventDefault();
  });

  $(document).on('dragover', function(e) {
    e.stopPropagation();
    e.preventDefault();
    droparea.css('border', '2px dotted #0B85A1');
  });

  $(document).on('drop', function(e) {
    e.stopPropagation();
    e.preventDefault();
  });
});
