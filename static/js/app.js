$(document).ready(function() {
  // Special thanks to http://www.it-view.net/drag-and-drop-file-upload-jquery-178.html
  function sendFileToServer(file) {
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
      $(html).prependTo(".samples").hide().fadeIn(1000);
    }
    fileReader.readAsDataURL(file);

    var formData = new FormData();
    formData.append('upfile', file);
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
      $(".result:first").html("Oops, something is wrong...");
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
    sendFileToServer(files[0]);
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

  $("#upload").click(function(e) {
    e.preventDefault();
    var file = $("#upfile")[0].files[0];
    // clear input type=file
    $('#upfile').replaceWith('<input type="file" id="upfile">');
    sendFileToServer(file);
  });
});
