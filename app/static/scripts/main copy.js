import TableCSV from "./TableCSV.js";

const tableRoot = document.querySelector("#csvRoot");
const csvFileInput = document.querySelector("#file");
const tableCsv = new TableCSV(tableRoot);

csvFileInput.addEventListener("change", (e) => {
  var fullPath = document.getElementById("file").value;
  if (fullPath) {
    var startIndex =
      fullPath.indexOf("\\") >= 0
        ? fullPath.lastIndexOf("\\")
        : fullPath.lastIndexOf("/");
    var filename = fullPath.substring(startIndex);
    if (filename.indexOf("\\") === 0 || filename.indexOf("/") === 0) {
      filename = filename.substring(1);
    }
  }
  $("#show_name_file").val(filename);
  Papa.parse(csvFileInput.files[0], {
    delimiter: ";",
    skipEmptyLines: true,
    complete: (results) => {
      $("#no_files").html("Total records: " + results.data.slice(1).length);
      tableCsv.update(results.data.slice(1, 3), results.data[0]);
    },
  });
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

$("#search_tracking").click(function () {
  var tracking_id = $("#tracking_id").val();
  $.get("search_tracking/" + tracking_id, function (data) {
    data = data[0];
    console.log(data);
    $("#return_info").html(
      `Adress Info: <hr> <hr> Fulfillment center: <br> Purchase Order: <br> SO Number: <br> Itern Symary: <br> Return Reason: <br> Total: ` +
        data.order_amount.replace("('", "").replace("',)", "")
    );
    $("#table_products").append(
      '<tr><td><i class="fas fa-image fa-3x"></i></td><td>' +
        data.merchant_SKU.replace("('", "").replace("',)", "") +
        "</td><td>" +
        data.order_quantity.replace("('", "").replace("',)", "") +
        '</td><td><button class="btn btn-primary">Manage</button></td></tr>'
    );
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

function blockUI(message) {
  $.blockUI({
    message:
      `<div class="lds-ellipsis">
        <div></div>
        <div></div>
        <div></div>
        <div></div>
      </div><br>
      <h2 id="text">` +
      message +
      `</h2>
      `,
    css: {
      border: "none",
      backgroundColor: "rgba(0, 0, 0, 0)",
    },
  });
}

function unblockUI(){
  $.unblockUI();
}
