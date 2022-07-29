function loadDataEdit(id, name, description, status) {
  $("#edit_id_provider").val(id);
  $("#edit_name").val(name);
  $("#edit_description").val(description);
  $("#edit_estatus").val(status);
  if (status == 2) {
    $("#activate_provider").show();
  }else{
    $("#activate_provider").hide();
  }
  $(".openModalEdit").click();
}

function loadDataNewFulfillment(id, name){
  $("#id_provider").val(id);
  $(".openModalNewFulfillment").click();
}

function loadDataDelete(id, name) {
  $("#delelete_id_provider").val(id);
  $("#span_name").html(name);
  $(".openModalDelete").click();
}

function show_fulfillment(id) {
  if ($("#table_fulfillment-" + id).is(":visible") == true) {
    $("#table_fulfillment-" + id).hide("fast");
  } else {
    $("#table_fulfillment-" + id).show("fast");
  }
}

function loadDataEditFulfillment(id, number, fulfillment_center, name, address, city, state, zip_code, status){
  $("#edit_store_number").val(number);
  $("#edit_fullfiment_center").val(fulfillment_center);
  $("#edit_store_name").val(name);
  $("#edit_address").val(address);
  $("#edit_city").val(city);
  $("#edit_state").val(state);
  $("#edit_zip_code").val(zip_code);
  $("#edit_id_fulfillment").val(id);
  $("#edit_estatus_fulfillment").val(status);
  if (status == 2) {
    $("#activate_fulfillment").show();
  }else{
    $("#activate_fulfillment").hide();
  }
  $(".openModalEditFulfillment").click();
}

function loadDataDeletefulfillment(id, name) {
  $("#delelete_id_fulfillment_center").val(id);
  $("#span_name_fulfillment").html(name);
  $(".openModalDeleteFulfillment").click();
}

$("#save-button-classification").click(function () {
  if (
    $("#name").val() != "" &&
    $("#description").val() != "" &&
    $("#status").val() != 0
  ) {
    blockUI("Save classification");
  }
  $(".save-submit").click();
});

$(".openModalEdit").click(function () {
  $("#modalEdit").modal("show");
});

$(".openModalDelete").click(function () {
  $("#modalDelete").modal("show");
});

$(".openModalNewFulfillment").click(function () {
  $("#modalNewFulfillment").modal("show");
});

$(".openModalEditFulfillment").click(function () {
  $("#modalEditFulfillment").modal("show");
});

$(".openModalDeleteFulfillment").click(function () {
  $("#modalDeleteFulfillment").modal("show");
});
