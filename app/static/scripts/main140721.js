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

function unblockUI() {
  $.unblockUI();
}

$("#close_alert").click(function () {
  $("#alert").hide();
});

function lootWeek(start_day, last_day){
  months_in_numbers = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"];
  const day = new Date().getDay();
  if (last_day >= day){
    var day_left = parseInt(last_day) - parseInt(day);
  }else{
    var day_left = (7 - parseInt(day)) + parseInt(last_day);
  }
  const l_date = new Date();
  const last_date = l_date.setDate(l_date.getDate() + day_left);
  var date = new Date();
  date.setTime(last_date);
  const start_date = date.setDate(date.getDate() - 6);

  var l = months_in_numbers[new Date(last_date).getMonth()]+""+("0"+new Date(last_date).getDate()).slice(-2);
  var s = months_in_numbers[new Date(start_date).getMonth()]+""+("0"+new Date(start_date).getDate()).slice(-2);
  return s + "-"+ l;
  //console.log(start_date);
}

function alert_message(message){
  $("#alert-text").html(message);
  $("#alert-message-success").show();
}

function alert_message_error(message){
  $("#alert-text").html(message);
  $("#alert-message-success").show();
}

$("#close_alert_success").click(function(){
  $("#alert-message-success").hide();
});

$("#close_alert_danger").click(function(){
  $("#alert-message-danger").hide();
});

function modal_alert(title, message){
  $("#modal-title").html(title);
  $("#modal-message").html(message);
  $("#modal-alert").modal("show");
}

$("#btn-close-modal-alert").click(function(){
  $("#modal-alert").modal("hide");
});

//Menu Selected
$(".menu a").click(function () {
  $(this).css("background-color","red");
});

$(".btn-close").click(function(){
  $(".modal-backdrop").removeClass("show");
  $(".modal-backdrop").removeClass("modal-backdrop");
});

$(".close_modal").click(function(){
  console.log("click");
  $(".modal-backdrop").removeClass("show");
  $(".modal-backdrop").removeClass("modal-backdrop");
});

function round(num, decimales = 2) {
  var signo = (num >= 0 ? 1 : -1);
  num = num * signo;
  if (decimales === 0) //con 0 decimales
    return signo * Math.round(num);
  // round(x * 10 ^ decimales)
  num = num.toString().split('e');
  num = Math.round(+(num[0] + 'e' + (num[1] ? (+num[1] + decimales) : decimales)));
  // x * 10 ^ (-decimales)
  num = num.toString().split('e');
  return signo * (num[0] + 'e' + (num[1] ? (+num[1] - decimales) : -decimales));
}