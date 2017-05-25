$(document).ready(function() {
  // Special thanks to http://www.it-view.net/drag-and-drop-file-upload-jquery-178.html
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
      dataType: "json"
    }).done(function(data, status, xhr) {
      console.log("ajax success!");
      $(".result:first").html("I'm " + data.prob
        + "% sure this is a <strong>" + data.kind + "</strong>");
    }).fail(function(xhr, status, error) {
      console.log("ajax failed!");
    });
  }

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
    var fileReader = new FileReader();
    fileReader.onload = function() {
      var dataUri = this.result;
      var html =
          "<tr>"
        + "  <td>"
        + "    <img src=\"" + dataUri + "\">"
        + "  </td>"
        + "  <td>"
        + "    <h2 class=\"result\">"
        + "      Loading..."
        + "    </h2>"
        + "  </td>"
        + "</tr>";
      $(".samples").prepend(html);
    }
    fileReader.readAsDataURL(files[0]);
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
