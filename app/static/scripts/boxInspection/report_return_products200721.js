var item_id_policy;
var containers = [];
var item;
var container = "";
var code_container;
var items_process = [];
var if_policy_a = false;
var items_excel = [];
var type_container = 0;
var info = {};

$("#daterange").change(function(){
  if($("#type").val()!=null){
    $("#type").change();
  }
});

$("#type").change(function () {
  blockUI("Searching...");
  var type = $("#type").val();
  $("#general_info").html(``);
  $("#tbodyItems").empty();
  type_container = 0;
  fulfillment_center_selected = 0;
  if (type == "policyaB") {
    type_container = 2;
  } else if (type == "policyaC") {
    type_container = 3;
  } else if (type == "policyaD") {
    type_container = 4;
  } else if (type == "policyaE") {
    type_container = 5;
  } else {
    type_container = 1;
    fulfillment_center_selected = type;
  }

  $("#search_by").html("Code/RGA");
  $("#tbodyContainers").empty();
  var range_date = $("#daterange").val()
  while (range_date.indexOf("/") >= 0) {
    var newStr = range_date.replace("/", "-");
    range_date = newStr;
  }
  $.get("search_lot_week/" + type + "/" + range_date, function (data) {
    if (type_container == 1) {
      var items = data.items;
      items.forEach((item) => {
        $("#table_container").append(
          `<tr><td onclick="selectContainer('` +
          item.rga +
          `')">` +
          item.rga +
          `</td></tr>`
        );
      });
      unblockUI();
    } else {
      if (type_container == 2) {

        $("#search_by").html("Filter by container");
      } else {
        $("#search_by").html("Filter by processed return code");
      }
      var items = data.items;
      if (type_container == 2) {
        items.forEach((item) => {
          $("#table_container").append(
            `<tr><td onclick="selectContainer('` +
            item.code +
            `')">` +
            item.code +
            `</td></tr>`
          );
        });
      } else {
        items.forEach((item) => {
          $("#table_container").append(
            `<tr><td onclick="selectContainer('` +
            item.id_processed_return +
            `')">` +
            item.id_processed_return +
            `</td></tr>`
          );
        });
      }
      unblockUI();
    }
  });
});

$("#lot_week").change(function () {
  alert(type_container);
  blockUI("Searching...");
  var lot_week = $("#lot_week").val();
  $("#tbodyContainers").empty();
  if (type_container == 1) {
    $("#search_by").html("Filter by RGA");
    $.get("search_items/1/" + lot_week + "/" + type_container, function (data) {
      var items = data.items;
      items.forEach((item) => {
        $("#table_container").append(
          `<tr><td onclick="selectContainer('` +
          item.rga +
          `')">` +
          item.rga +
          `</td></tr>`
        );
      });
      unblockUI();
    });
  } else {
    if (type_container == 2) {

      $("#search_by").html("Filter by container");
    } else {
      $("#search_by").html("Filter by processed return code");
    }
    console.log("http://127.0.0.1:801/report_return_products/" + "search_items/2/" + lot_week + "/" + type_container);
    $.get("search_items/2/" + lot_week + "/" + type_container, function (data) {
      var items = data.items;
      if (type_container == 2) {
        items.forEach((item) => {
          $("#table_container").append(
            `<tr><td onclick="selectContainer('` +
            item.code +
            `')">` +
            item.code +
            `</td></tr>`
          );
        });
      } else {
        items.forEach((item) => {
          $("#table_container").append(
            `<tr><td onclick="selectContainer('` +
            item.id_processed_return +
            `')">` +
            item.id_processed_return +
            `</td></tr>`
          );
        });
      }

      unblockUI();
    });
  }
});

function selectContainer(code) {
  blockUI("Search information");
  $("#tbodyItems").empty();
  $.get("search_information/" + type_container + "/" + code, function (data) {
    var general_info = data.general_info[0];
    if (type_container == 1) {
      $("#general_info").html(
        `<strong>RGA code: </strong>` +
        general_info.rga +
        `<br><strong>Container code: </strong>` +
        general_info.container__code +
        `<br><strong>Processed date: </strong>` +
        general_info.processed_return__c_date +
        `<br><strong>User: </strong>` +
        general_info.c_user__username +
        `<br><strong>Fulfillment center return: </strong>` +
        general_info.fulfillment_center+
        `<br><br><p class="btn btn-primary" onclick="downloadDocument();">Download document</p>`
      );
    } else if (type_container == 2) {
      $("#general_info").html(
        `<strong>Policy code: </strong>` +
        general_info.rga +
        `<br><strong>Container code: </strong>` +
        general_info.container__code +
        `<br><strong>Processed date: </strong>` +
        general_info.processed_return__c_date +
        `<br><strong>User: </strong>` +
        general_info.c_user__username +
        `<br><br><p class="btn btn-primary" onclick="downloadDocument();">Download document</p>`
      );
    } else if (type_container == 3) {
      $("#general_info").html(
        `<strong>Processed return code: </strong>` +
        general_info.processed_return__id_processed_return +
        `<br><strong>Processed date: </strong>` +
        general_info.processed_return__c_date +
        `<br><strong>User: </strong>` +
        general_info.c_user__username +
        `<br><br><p class="btn btn-primary" onclick="downloadDocument();">Download document</p>`
      );
    } else {
      $("#general_info").html(
        `<strong>Processed return code: </strong>` +
        general_info.processed_return__id_processed_return +
        `<br><strong>Processed date: </strong>` +
        general_info.processed_return__c_date +
        `<br><strong>User: </strong>` +
        general_info.c_user__username +
        `<br><br><p class="btn btn-primary" onclick="downloadDocument();">Download document</p>`
      );
    }

    var items = data.items;
    items_excel = [];
    info = {container_code: general_info.container__code, user: general_info.c_user__username, classification_date:general_info.processed_return__c_date}
    $("#table_products").empty();
    if(type_container == 3){
      tableHeaderC();
      items.forEach((item) => {
        items_excel.push({ id: item.item_id, rga: item.rga });
        items_process.push({ id: item.item_id, name:"", rga: "", selected: true, total: item.total, discount: item.final_price, percentage: item.percentage , sku: item.sku, quantity: item.quantity , so: item.so, po: item.po, container_code:item.container__code });
        $("#table_products").append(
          `<tr><td>` +
          item.sku +
          `</td><td>` +
          item.item_summary +
          `</td><td>` +
          item.container__code +
          `</td><td>` +
          item.quantity +
          `</td><td>` +
          item.total +
          `</td><td>` +
          item.percentage +
          `</td><td>` +
          item.final_price +
          `</td></tr>`
        );
      });
    }else{
      tableHeaderOther();
      items.forEach((item) => {
        items_excel.push({ id: item.item_id, rga: item.rga });
        items_process.push({ id: item.item_id, name: "", rga: "", selected: true, total: item.total, discount: item.final_price, percentage: item.percentage , sku: item.sku, quantity: item.quantity , so: item.so, po: item.po, container_code:item.container__code });
        $("#table_products").append(
          `<tr><td>` +
          item.sku +
          `</td><td>` +
          item.item_summary +
          `</td><td>` +
          item.container__code +
          `</td><td>` +
          item.quantity +
          `</td><td>` +
          item.so +
          `</td><td>` +
          item.po +
          `</td></tr>`
        );
      });
    }
    
    unblockUI();
  });
}

function tableHeaderOther() {
  $("#table_products").append(
    `<thead id="tHeadItems">
    <th>SKU</th>
    <th>Name product</th>
    <th>Container</th>
    <th>Quantity</th>
    <th>SO</th>
    <th>PO</th>
  </thead>
  <tbody id="tbodyItems"></tbody>`
  )
}

function tableHeaderC() {
  $("#table_products").append(
    `<thead id="tHeadItems">
    <th>SKU</th>
    <th>Name product</th>
    <th>Container</th>
    <th>Quantity</th>
    <th>Cost</th>
    <th>Discount rate(%)</th>
    <th>Final price </th>
  </thead>
  <tbody id="tbodyItems"></tbody>`
  )
}

function downloadDocument() {
  blockUI("Generated document");
  if(type_container == 1){
    var a = document.createElement('a');
    var file_name = "RGA.xlsx";
    a.href = "/return_products/generated_excel/" + JSON.stringify(items_excel)+"/2/";
    a.download = file_name;
    a.click();
    unblockUI();
  }
  if(type_container == 2){
    var a = document.createElement('a');
    var file_name = "Policy A.xlsx";
    a.href = "/return_products/generated_excel/" + JSON.stringify(items_excel)+"/1/";
    a.download = file_name;
    a.click();
    unblockUI();
  }else if (type_container == 3) {
    var a = document.createElement('a');
    var file_name = "Policy A Grade C.pdf";
    console.log("http://127.0.0.1:801/report_return_products/generated_pdf/3/"+JSON.stringify(items_process)+"/"+JSON.stringify(info));
    a.href = "generated_pdf/3/"+JSON.stringify(items_process)+"/"+JSON.stringify(info);
    console.log(a.href)
    a.download = file_name;
    a.click();
    unblockUI();
  }else if (type_container == 4) {
    var a = document.createElement('a');
    var file_name = "Policy A Grade D.pdf";
    a.href = "generated_pdf/4/"+JSON.stringify(items_process)+"/"+JSON.stringify(info);
    console.log(a.href)
    a.download = file_name;
    a.click();
    unblockUI();
  }else if (type_container == 5) {
    var a = document.createElement('a');
    var file_name = "Policy A Grade E.pdf";
    a.href = "generated_pdf/5/"+JSON.stringify(items_process)+"/"+JSON.stringify(info);
    console.log(a.href)
    a.download = file_name;
    a.click();
    unblockUI();
  }
  
}

$(function () {
  const firstdate = moment().startOf('month').format('MM/DD/YYYY');
  const lastdate = moment().endOf('month').format("MM/DD/YYYY");
  $("#daterange").val(firstdate + " - " + lastdate);
  $('input[name="daterange"]').daterangepicker({
    opens: 'left'
  }, function (start, end, label) {
  });
});
