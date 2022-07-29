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

function loadDataEdit(id, name, description, status) {
  $("#edit_id_classification").val(id);
  $("#edit_name").val(name);
  $("#edit_description").val(description);
  $("#edit_description").val(description);
  $("#edit_estatus").val(status);
  if (status == 2) {
    $("#activate_classification").show();
  }
  $(".openModalEdit").click();
}

function loadDataDelete(id, name) {
  $("#delelete_id_classification").val(id);
  $("#span_name").val(name);
  $(".openModalDelete").click();
}

$("#close_alert").click(function () {
  $("#alert").hide();
});

$("#save-button-classification").click(function () {
  if (
    $("#name").val() != "" &&
    $("#description").val() != "" &&
    $("#status").val() != 0
  ) {
    $.blockUI({
      message: `<div class="lds-ellipsis">
      <div></div>
      <div></div>
      <div></div>
      <div></div>
    </div><br>
    <h2 id="text">Upload info</h2>
    `,
      css: {
        border: "none",
        backgroundColor: "rgba(0, 0, 0, 0)",
      },
    });
  }
  $(".save-submit").click();
});

$("#save-button-records").click(function () {
  if ($("#file").val() != "") {
    $.blockUI({
      message: `<div class="lds-ellipsis">
      <div></div>
      <div></div>
      <div></div>
      <div></div>
    </div><br>
    <h2 id="text">Upload info</h2>
    `,
      css: {
        border: "none",
        backgroundColor: "rgba(0, 0, 0, 0)",
      },
    });
  }
  $(".save-submit").click();
});

$("#save-button").click(function () {
  cxt.drawImage(video, 0, 0, 300, 150);
  var data = canvas.toDataURL("image/jpeg");
  var info = data.split(",", 2);
  //console.log(checkCamera());
  if (checkCamera()) {
    $("#photography").val(info);
  }
  $("#load_info").addClass("blocker");
  $(".save-submit").click();
});

$(".openModalEdit").click(function () {
  $("#modalEdit").modal("show");
});

$(".openModalDelete").click(function () {
  $("#modalDelete").modal("show");
});

$(".openModal").click(function () {
  $("#modalImage").modal("show");
});

function openModalManage(){
  alert("HOLA");
  $("#modalManage").modal("show");
}

$("#search_tracking").click(function () {
  var tracking_id = $("#tracking_id").val();
  $.get("search_tracking/" + tracking_id, function (data) {
    data = data[0];
    $("#tbodyProducts").empty();
    if (data.status == 400) {
      $("#return_info").html(`<p style="color:red">Record not found</p>`);
    } else {
      $("#return_info").html(
        `<strong>Address Info</strong>: <hr> <hr> <strong>Fulfillment center</strong>: <br> <strong>Purchase Order</strong>: <br> <strong>SO Number</strong>: <br> <strong>Item Sumary</strong>: ` +
          data.merchant_SKU.replace("('", "").replace("',)", "") +
          ` <br> <strong>Return Reason</strong>:` +
          data.return_reason.replace("('", "").replace("',)", "") +
          ` <br> <strong>Total</strong>: ` +
          data.order_amount.replace("('", "").replace("',)", "")
      );
      $("#table_products").append(
        '<tr><td><i class="fas fa-image fa-3x"></i></td><td>' +
          data.merchant_SKU.replace("('", "").replace("',)", "") +
          "</td><td>" +
          data.order_quantity.replace("('", "").replace("',)", "") +
          '</td><td><button class="btn btn-primary openModalManage" data-toggle="modal" data-target="#modalManage" id="openModalManage" onclick="openModalManage();">Manage</button></td></tr>'
      );
    }
  });
});

$(document).ready(function () {
  $(window).keydown(function (event) {
    if (event.keyCode == 13) {
      $("#save-button").click();
      event.preventDefault();
      return false;
    }
  });
});
