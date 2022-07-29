function loadDataEdit(id, name, description, status, return_provider, existence) {
  $("#edit_id_classification").val(id);
  $("#edit_name").val(name);
  $("#edit_description").val(description);
  $("#edit_estatus").val(status);
  $("#edit_existence").val(existence);
  $("#edit_existence").change();
  $("#edit_return_provider").val(return_provider);
  if (status == 2) {
    $("#activate_classification").show();
  }else{
    $("#activate_classification").hide();
  }
  $(".openModalEdit").click();
}

function loadDataDelete(id, name) {
  $("#delelete_id_classification").val(id);
  $("#span_name").html(name);
  $(".openModalDelete").click();
}

$("#save-button-classification").click(function () {
  if($("#existence").val()==null){
    alert("Please select a value to if this classification contains existence");
    return;
  }
  if($("#return_provider").val()==null){
    alert("Please select a value to if return to provider");
    return;
  }
  if (
    $("#name").val() != "" &&
    $("#description").val() != "" &&
    $("#status").val() != 0 &&
    $("#return_provider").val() != null
  ) {
    blockUI("Save classification");
  }
  $(".save-submit").click();
});

$("#existence").change(function(){
  var val = $("#existence").val();
  if(val == "2"){
    $("#return_provider").val("2");
    $("#return_provider").hide();
    $("#return_provider_disabled").show();
  }else{
    $("#return_provider").val("0");
    $("#return_provider").show();
    $("#return_provider_disabled").hide();
  }
});

$("#edit_existence").change(function(){
  var val = $("#edit_existence").val();
  if(val == "2"){
    $("#edit_return_provider").val("2");
    $("#edit_return_provider").hide();
    $("#edit_return_provider_disabled").show();
  }else{
    $("#edit_return_provider").val("0");
    $("#edit_return_provider").show();
    $("#edit_return_provider_disabled").hide();
  }
});

$(".openModalEdit").click(function () {
  $("#modalEdit").modal("show");
});

$(".openModalDelete").click(function () {
  $("#modalDelete").modal("show");
});
