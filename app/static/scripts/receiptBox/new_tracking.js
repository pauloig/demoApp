$("#save-button").click(function () {
  if ($("#id_tracking").val() != "" && $("#shipping_tracking").val() != undefined) {
    blockUI("Saving tracking...");
  }

  cxt.drawImage(video, 0, 0, 300, 150);
  var data = canvas.toDataURL("image/jpeg");
  var info = data.split(",", 2);
  if (checkCamera()) {
    $("#photography").val(info);
  }
  $(".save-submit").click();
});

$(".openModal").click(function () {
  $("#modalManage").modal("show");
});

$("#close-modal").click(function(){
  $("#modalImage").modal("hide");
  $('body').removeClass('modal-open');
  $('.modal-backdrop').remove();
});

function selectRadio(id_radio) {
  $(".form-check").removeClass("selected");
  $("#form-check-" + id_radio).addClass("selected");
}

function loadImage(image, no_tracking, shipping_service, user, date) {
  $("#image-tracking").attr("src", image);
  $("#modal_no_tracking").html(no_tracking);
  $("#modal_return_service").html(shipping_service);
  $("#modal_user").html(user);
  $("#modal_date").html(date);
  $(".openModal").click();
}

$(document).ready(function () {
  $(window).keydown(function (event) {
    if (event.keyCode == 13) {
      $("#save-button").click();
      event.preventDefault();
      return false;
    }
  });
});
