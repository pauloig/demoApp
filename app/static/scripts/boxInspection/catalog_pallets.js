var code_print = "";
function loadDataEdit(
  code,
  lot_week,
  description,
  type,
  classification,
  fulfillment_center,
  status
) {
  $("#edit_id_container").val(code);
  $("#edit_lot_week").val(lot_week);
  $("#edit_description").val(description);
  $("#edit_type").val(type);
  $("#edit_classification").val(classification);
  if (fulfillment_center != "") {
    $("#edit_fulfillment_center").val(fulfillment_center);
  } else {
    $("#edit_fulfillment_center").val(
      $("#edit_fulfillment_center").prop("selectedIndex", 1).val()
    );
  }
  $("#edit_estatus").val(status);
  $("#edit_classification").change();
  $(".openModalEdit").click();
}

function loadDataDelete(code, lot_week) {
  $("#disabled_id_container").val(code);
  $("#span_name").html(code);
  $(".openModalDelete").click();
}

function loadCodeBar(code, lot_week) {
  code_print = code;
  JsBarcode("#barcode", code, {
    width: 1.5,
    height: 100,
    fontSize: 20,
    displayValue: true,
  });

  $("#id_codebar").val(code);
  $("#l_lot_week").html(lot_week);
  $(".openModalCodebar").click();
}

$(document).ready(function () {
  var start_date = $("#start_date").val();
  var last_date = $("#last_date").val();
  var lot_week = lootWeek(start_date, last_date);
  $("#lot_week_disabled").val("Lot week: "+lot_week);
  $("#lw").val(lot_week);
  $("#lot_week").prop("disabled", true);
  $("#classification").change();
});

$("#classification").change(function () {
  var classification = $("#classification").val();
  if (classification != null) {
    classification = classification.split("-");
    if (classification[0] == "1") {
      $("#fulfillment_center_form").show();
    } else {
      $("#fulfillment_center_form").hide();
    }
  }
});

$(".openModalEdit").click(function () {
  $("#modalEdit").modal("show");
});

$(".openModalDelete").click(function () {
  $("#modalDelete").modal("show");
});

$(".openModalCodebar").click(function () {
  $("#modalCodeBar").modal("show");
});

$("#btn_print_codebar").click(function () {
  const element = document.getElementById("zone_print");
  //console.log(element);
  var opt = {
    filename: "Barcode-"+code_print+".pdf",
    image: { type: "jpeg", quality: 0.98 },
    jsPDF: { unit: "in", format: [3, 2], orientation: "landscape" },
    scale: 1,
  };
  html2pdf().set(opt).from(element).save();
  // window.open('/print_codebar/'+$("#id_codebar").val(), '_blank');
});

$("#save-button").click(function () {
  if ($("#type").val() == null) {
    alert("Please, select a type container");
    return;
  }
  if ($("#classification").val() == null) {
    alert("Please, select a classification");
    return;
  }
  var classification = $("#classification").val();
  classification = classification.split("-");
  if (classification[0] == "1") {
    if ($("#fulfillment_center").val() == null) {
      alert("Please, select a fulfillment center");
      return;
    }
  } else {
    $("#fulfillment_center").prop("selectedIndex", 1).val();
  }
  var manual_code = $("#manual_code").val();
  if(manual_code == ""){
    manual_code = "manual_code";
  }
  $.get(
    "verification_container/" +
      $("#fulfillment_center").val() +
      "/" +
      $("#type").val() +
      "/" +
      $("#classification").val()+"/"+manual_code,
    function (data) {
      console.log(data);
      if (data.status == "True") {
        if(data.type == 2){
          info = data.container[0];
          $("#code_container_closed").html(info.code);
          console.log(info.classification__return_provider);
          if(info.type = "T"){
            type = "Tote";
          }else{
            type = "Pallet";
          }
          if (info.classification__return_provider == 1) {
            $("#detail_close_containers").html(
              `<strong>Code: </strong> ` +
                info.code +
                `<br><strong>Lot Week: </strong> ` +
                info.lot_week +
                `<br><strong>Type: </strong> ` +
                type +
                `<br><strong>Classification: </strong> ` +
                info.classification__name
            );
          } else {
            $("#detail_close_containers").html(
              `<strong>Code: </strong> ` +
                info.code +
                `<br><strong>Lot Week: </strong> ` +
                info.lot_week +
                `<br><strong>Type: </strong> ` +
                type +
                `<br><strong>Classification: </strong> ` +
                info.classification__name +
                `<br><strong>Fulfillment Center: </strong> ` +
                info.fulfillment_center__fulfillment_center
            );
          }
          $("#modalConfirmSave").modal("show");
        }else{
          modal_alert("Repeated code", "The code I entered has already been entered previously.");
        }
        
      } else {
        $("#save-submit").click();
      }
    }
  );
  //$("#save-submit").click();
});

$("#close_modal_confirm").click(function () {
  $("#modalConfirmSave").modal("hide");
});

$("#close_modal_close_container").click(function () {
  $("#modalDelete").modal("hide");
});

$("#save_form_container").click(function () {
  $("#save-submit").click();
});

$("#close_codebar_modal").click(function(){
  $("#modalCodeBar").modal("hide");
})

$("#edit_classification").change(function () {
  var classification = $("#edit_classification").val();
  classification = classification.split("-");
  if (classification[0] == "1") {
    $("#edit_fulfillment_center_form").show();
  } else {
    $("#edit_fulfillment_center_form").hide();
  }
});
