var item_id_policy;
var containers = [];
var item;
var container = "";
var code_container;
var items_process = [];
var type_container = 0;
var fulfillment_center_selected = 0;
var info = {};

$("#fulfillment_center").change(function () {
  blockUI("Searching containers");
  validateDataReclassification();
  $("#table_products").empty();
  var fc = $("#fulfillment_center").val();
  type_container = 0;
  fulfillment_center_selected = 0;
  if (fc == "policyaB") {
    type_container = 2;
  } else if (fc == "policyaC") {
    type_container = 3;
  } else if (fc == "policyaD") {
    type_container = 4;
  } else if (fc == "policyaE") {
    type_container = 5;
  } else {
    type_container = 1;
    fulfillment_center_selected = fc;
  }

  $("#tbodyContainers").empty();
  $.get("search_container/fulfillment_center/" + fc, function (data) {
    var containers = data.container;
    if (containers.length == 0) {
      $("#table_container").append('<tr><td><label>Records not found</label></td></tr>')
    }
    containers.forEach((container) => {
      if (type_container == 1 || type_container == 2) {
        $("#table_container").append(
          `<tr><td onclick="selectContainer('` +
          container.code +
          `')">` +
          container.code +
          `</td></tr>`
        );
      } else {
        $("#table_container").append(
          `<tr><td onclick="selectContainer('` +
          container.lot_week +
          `')">` +
          container.lot_week +
          `</td></tr>`
        );
      }
    });
    unblockUI();
  });
});

$("#re_classification").click(function () {
  var cont_reclassified = 0;
  var sku_listing = "";
  items_process.forEach(item => {
    if (item.selected) {
      sku_listing += ", " + item.sku;
      cont_reclassified++;
    }
  });
  $("#sku_listing_to_reclassification").html("<strong> Sku listing to re classified: </strong>" + sku_listing.substr(2));
  $("#count_sku_to_reclassfied").html("Quantity: " + cont_reclassified);
  $("#sku_listing_to_reclassification")
  $("#modalReClassificationInLot").modal("show");
});

function selectContainer(code) {
  items_process = [];
  blockUI("Search products");
  $("#table_products").empty();
  if (type_container == 3) {
    tableHeaderC();
  } else {
    tableHeaderOther();
  }
  $.get("search_order_sales/" + code + "/" + type_container + "/" + fulfillment_center_selected, function (data) {
    var items = data.items;
    var cont = 0;

    items.forEach((item) => {
      if (type_container == 3) {
        $("#tbodyItems").append(
          "<tr id='select-" +
          cont +
          "'><td style='text-align:center;'><input id='checkbox-" + cont + "' type='checkbox' onclick='selectRow(" +
          cont +
          `);'  class='form-check-input'></td><td class='selectionable' id='sku_select-` +
          cont +
          `' onclick='copy_to_clipboard("sku_select-` +
          cont +
          `");'>` +
          item.sku +
          "</td><td>" +
          item.item_summary +
          `</td><td>` +
          item.container__code +
          `</td><td width="150"><input  type="number" min="1" max="` + item.quantity + `" value="` + item.quantity + `" class="form-control" id="quantity-` + cont + `" onkeyup="calculate_percentage(` + cont + `);" onchange="calculate_percentage(` + cont + `);" placeholder="Quantity sale"></td><td>` +
          item.total +
          `</td><td width="150"><input  type="number" class="form-control" min="0" max="100" id="percentage-` + cont + `" onkeyup="calculate_percentage(` + cont + `);" placeholder="Discount rate"></td><td
          '><label id="total_discount-`+ cont + `">0.00</label></td><td><button class="btn btn-danger btn-rounded btn-floating" onclick="policyA('` +
          item.item_id +
          `');"><i class="fas fa-people-carry"></i></button></td><td style="display:none;">` +
          item.comments +
          `</td></tr>`
        );
      } else {
        $("#tbodyItems").append(
          "<tr id='select-" +
          cont +
          "'><td style='text-align:center;'><input id='checkbox-" + cont + "' type='checkbox' onclick='selectRow(" +
          cont +
          `);'  class='form-check-input'></td><td class='selectionable' id='sku_select-` +
          cont +
          `' onclick='copy_to_clipboard("sku_select-` +
          cont +
          `");'>` +
          item.sku +
          "</td><td>" +
          item.item_summary +
          `</td><td>` +
          item.container__code +
          `</td><td>` +
          item.quantity +
          `</td><td class='selectionable' id='so_select-` +
          cont +
          `' onclick='copy_to_clipboard("so_select-` +
          cont +
          `");'>` +
          item.so +
          `</td><td class='selectionable' id='po_select-` +
          cont +
          `' onclick='copy_to_clipboard("po_select-` +
          cont +
          `");'>` +
          item.po +
          `</td><td><button class="btn btn-danger btn-rounded btn-floating" onclick="policyA('` +
          item.item_id +
          `');"><i class="fas fa-people-carry"></i></button></td><td style="display:none;">` +
          item.comments +
          `</td></tr>`
        );
      }

      items_process.push({ id: item.item_id, name: "", rga: "", selected: false, total: item.total, discount: 0.00, percentage: 0.00, sku: item.sku, quantity: item.quantity, so: item.so, po: item.po, container_code: item.container__code });
      cont++;
    });
    if (items.length != 0) {
      let date = new Date()
      let day = date.getDate()
      let month = date.getMonth() + 1
      let year = date.getFullYear()

      if (month < 10) {
        date_today = (`${year}-${month}-0${day}`)
      } else {
        date_today = (`${year}-${month}-${day}`)
      }
      info = { container_code: items[0].container__code, user: items[0].c_user__username, classification_date: date_today }
      $("#select_all").attr("disabled", false);
      if (type_container == 3) {
        $("#table_products").append(
          `<tr><td colspan="8"></td><td><button class="btn btn-danger" id="save_rga" onclick="save_rga();">Save</button></td></tr>`
        );
      } else {
        $("#table_products").append(
          `<tr><td colspan="7"></td><td><button class="btn btn-danger" id="save_rga" onclick="save_rga();">Save</button></td></tr>`
        );
      }
    } else {
      $("#select_all").attr("disabled", true);
      $("#select_all").prop("checked", false);
    }
    unblockUI();
  });
}

function calculate_percentage(item_row) {
  var percentage = $("#percentage-" + item_row).val() / 100;
  if ($("#percentage-" + item_row).val() >= 100) {
    $("#percentage-" + item_row).val(100);
    calculate_percentage(item_row);
    percentage = 1;
  }
  var quantity = $("#quantity-" + item_row).val();
  if (quantity < 1) {
    $("#quantity-" + item_row).val(1);
    calculate_percentage(item_row);
  }
  var total = items_process[item_row].total;
  var discount = (total - (total * percentage)) * quantity;
  items_process[item_row].discount = round(discount);
  items_process[item_row].percentage = $("#percentage-" + item_row).val();
  items_process[item_row].quantity = quantity;
  $("#total_discount-" + item_row).html(String(round(discount)));
}

function tableHeaderOther() {
  $("#table_products").append(
    `<thead id="tHeadItems">
    <th style="text-align: center;"><input onclick="select_all();" type="checkbox" name="select_all" id="select_all" class='form-check-input' disabled></th>
    <th>SKU</th>
    <th>Product name</th>
    <th>Container</th>
    <th>Quantity</th>
    <th>SO</th>
    <th>PO</th>
    <th>Reclassification</th>
    <th style="display: none;">UPC</th>
  </thead>
  <tbody id="tbodyItems"></tbody>`
  )
}

function tableHeaderC() {
  $("#table_products").append(
    `<thead id="tHeadItems">
    <th style="text-align: center;"><input onclick="select_all();" type="checkbox" name="select_all" id="select_all" class='form-check-input' disabled></th>
    <th>SKU</th>
    <th>Product name</th>
    <th>Container</th>
    <th>Quantity</th>
    <th>Cost</th>
    <th>Discount rate(%)</th>
    <th>Final price </th>
    <th>Reclassification</th>
    <th style="display: none;">UPC</th>
  </thead>
  <tbody id="tbodyItems"></tbody>`
  )
}

function select_all() {
  if ($("#select_all").is(':checked')) {
    cont = 0;
    items_process.forEach(item => {
      $("#checkbox-" + cont).prop("checked", true)
      item.selected = true;
      $("#select-" + cont).addClass("selected-row");
      cont++;
    });
    $(".select_all").hide();
    $(".unselect_all").show();
  } else {
    cont = 0;
    items_process.forEach(item => {
      $("#checkbox-" + cont).prop("checked", false)
      item.selected = false;
      $("#select-" + cont).removeClass("selected-row");
      cont++;
    });
    $(".select_all").show();
    $(".unselect_all").hide();
  }
  validateOptionReclassification();
}

function copy_to_clipboard(element) {
  var text = $("#" + element).html();
  var f_c = text.substr(0, 3);
  if (f_c == "ACE" || f_c == "EJD") {
    text = text.substr(4, 11);
  }
  if (f_c == "JEN") {
    text = text.substr(4, 8) + "" + text.substr(9, 13);
  }

  var id = "temporary_id";
  var existsTextarea = document.getElementById(id);

  if (!existsTextarea) {
    var textarea = document.createElement("textarea");
    textarea.id = id;
    textarea.style.position = "fixed";
    textarea.style.top = 0;
    textarea.style.left = 0;

    textarea.style.width = "1px";
    textarea.style.height = "1px";

    textarea.style.padding = 0;

    textarea.style.border = "none";
    textarea.style.outline = "none";
    textarea.style.boxShadow = "none";

    textarea.style.background = "transparent";
    document.querySelector("body").appendChild(textarea);
    existsTextarea = document.getElementById(id);
  } else {
    console.log("El textarea ya existe");
  }

  existsTextarea.value = text;
  existsTextarea.select();

  try {
    var status = document.execCommand("copy");
    if (!status) {
      alert_message_error("Error on copy to clipboard");
    } else {
      alert_message("Copy to clipboard");
    }
  } catch (err) {
    alert_message_error("Error on copy to clipboard");
  }
}

function excepcion() {
  alert("Error on copy to clipboard");
}

function save_rga() {
  all_items_was_selected = true;
  var cont_selected = 0;
  var list_containers_string = "";
  items_process.forEach((item) => {
    if (item.selected == false) {
      all_items_was_selected = false;
    }
    if (item.selected) {
      cont_selected++;
    }
    list_containers_string += ", " + item.container_code;
  });
  list_containers_string = list_containers_string.slice(2);
  if (type_container == 3 || type_container == 4 || type_container == 5) {
    submit_items();
    all_items_was_selected = true;
  } else {
    if (all_items_was_selected) {

      $("#count_rows").html(
        "<label><Strong>Total row products: </strong>" + cont_selected + "</label>"
      );
      $("#container_code").html(
        "<label><Strong>Container code: </strong>" + list_containers_string + "</label>"
      );
      $("#modalProcess").modal("show");
      if (type_container == 1) {
        $("#titleModal").html("Grade A");
        $("#policy_form").hide();
        $("#rga_form").show();
        $("#code_rga").val("");
        $("#policy_a_code").val("");
      } else {
        $("#titleModal").html("Policy A");
        $("#rga_form").hide();
        $("#policy_form").show();
        $("#code_rga").val("");
        $("#policy_a_code").val("");
      }
    } else {
      alert("Products are missing to process, please check again");
    }
  }
}

function submit_items() {
  if (!type_container) {
    if ($("#code_rga").val() == "") {
      alert("Please insert a value in RGA code");
      return;
    }
  }
  blockUI("Save data");
  items_process.forEach((item) => {
    if ($("#code_rga").val() != "") {
      item.rga = $("#code_rga").val();
    } else {
      item.rga = $("#policy_a_code").val();
    }
  });
  $("#items").val(JSON.stringify(items_process));
  $("#type_container").val(type_container);
  $("#code_container_form").val(code_container);
  $("#general_info").val(info);
  if (type_container == 2) {
    var a = document.createElement('a');
    var file_name = "Policy A Grade B.xlsx";
    a.href = "generated_excel/" + JSON.stringify(items_process)+"/1/";
    console.log(a.href);
    a.download = file_name;
    a.click();
    $("#process_form").submit();
    unblockUI();
  } if (type_container == 3) {
    var a = document.createElement('a');
    var file_name = "Policy A Grade C.pdf";
    a.href = "generated_pdf/3/" + JSON.stringify(items_process) + "/" + JSON.stringify(info);
    console.log(a.href)
    a.download = file_name;
    a.click();
    $("#process_form").submit();
    unblockUI();
  } if (type_container == 4) {
    var a = document.createElement('a');
    var file_name = "Policy A Grade D.pdf";
    a.href = "generated_pdf/4/" + JSON.stringify(items_process) + "/" + JSON.stringify(info);
    console.log(a.href)
    a.download = file_name;
    a.click();
    $("#process_form").submit();
    unblockUI();
  } if (type_container == 5) {
    var a = document.createElement('a');
    var file_name = "Policy A Grade E.pdf";
    a.href = "generated_pdf/5/" + JSON.stringify(items_process) + "/" + JSON.stringify(info);
    console.log(a.href)
    a.download = file_name;
    a.click();
    $("#process_form").submit();
    unblockUI();
  } else {
    var a = document.createElement('a');
    var file_name = "RGA.xlsx";
    a.href = "generated_excel/" + JSON.stringify(items_process)+"/2/";
    console.log(a.href);
    a.download = file_name;
    a.click();
    $("#process_form").submit();
  }
}

function selectRow(id) {
  if ($("#select-" + id).hasClass("selected-row")) {
    items_process[id].selected = false;
    $("#select-" + id).removeClass("selected-row");
  } else {
    items_process[id].selected = true;
    $("#select-" + id).addClass("selected-row");
  }
  validateOptionReclassification();
}

function validateOptionReclassification() {
  var items_selected = false;
  items_process.forEach(item => {
    if (item.selected) {
      items_selected = true;
    }
  });
  if (items_selected) {
    $("#re_classification").attr("disabled", false);
  } else {
    $("#re_classification").attr("disabled", true);
  }
}

function process(item_id) {
  var policy_code = $("#policy_code-" + item_id).val();
  if (policy_code == "") {
    alert("Please, insert a value in policy code");
    return;
  }
  blockUI("Process policy code");
  $.get("process_sale_order/" + item_id + "/" + policy_code, function (data) {
    if (data.status == 1) {
      alert_message(data.message);
    }
  });
  unblockUI();
}

function policyA(item_id) {
  item_id_policy = item_id;
  $("#modalManage").modal("show");
  $("#description").val("");
  $("#form-container").hide();
  $("#container").val("");
}

function selectClassification(
  id_classification,
  name,
  description,
  existence,
  return_provider
) {
  blockUI("Searching containers");
  $.get(
    "search_container/classification/" + id_classification,
    function (data) {
      containers = data.container;
      $("#classification_selected").html("Selected: " + name);
      $("#classification_description").html(description);
      $("#info-classification").show();
      $("#form-classification").hide();
      if (existence == 1) {
        $("#form-container").show();
        $("#container").focus();
        $("#container").val("");
      } else {
        container = "WE";
        $("#container").val("Without existence");
      }
      unblockUI();
      validateData();
    }
  );
}

$("#container").keyup(function (e) {
  if (e.keyCode == 13) {
    $("#message").html("");
    var container_val = $("#container").val();
    var find_container = false;
    var container_lot_week;
    var container_code;
    var return_provider = true;
    var fulfillment_center = "";
    containers.forEach((container) => {
      if (container.code == container_val) {
        find_container = true;
        container_lot_week = container.lot_week;
        container_code = container.code;
        if (container.classification__return_provider == 1) {
          return_provider = true;
        } else {
          return_provider = false;
        }
        fulfillment_center = container.fulfillment_center__fulfillment_center;
      }
    });
    container = "";
    if (find_container) {
      var last_date = $("#last_date").val();
      var lot_week = lootWeek("", last_date);
      // if (container_lot_week == lot_week) {
      if (!return_provider) {
        container = container_code;
        console.log("OK");
      } else {
        if (fulfillment_center == items[item_select].fulfillment_center) {
          container = container_code;
          console.log("OK");
        } else {
          $("#message").html(
            "This product does not belong to this fulfillment center."
          );
        }
      }
      // } else {
      //   $("#message").html("The lot week is not correct, try other code.");
      // }
    } else {
      $("#message").html(
        "This container not found in this classification, try other code."
      );
    }
    validateData();
  }
});

function validateData() {
  if (container != "") {
    $("#save-policy").prop("disabled", false);
  } else {
    $("#save-policy").prop("disabled", true);
  }
}

$("#save-policy").click(function () {
  blockUI("Save policy A");
  $.get("policy-a/" + item_id_policy + "/" + container, function (data) {
    if (data.status == 1) {
      $("#fulfillment_center").change();
      selecteOther();
      selectContainer(code_container);
      $("#modalManage").modal("hide");
      alert_message(data.message);
    }
  });
  unblockUI();
});

function selecteOther() {
  container = "";
  $("#container").val("");
  $("#containers_info").html("");
  $("#info-classification").hide();
  $("#form-classification").show();
  $("#form-container").hide();
  $("#message").html("");
  validateData();
}

document.querySelector("#buscar").onkeyup = function () {
  console.log("HOLA");
  $TableFilter("#table_products", this.value);
}

$TableFilter = function (id, value) {
  var rows = document.querySelectorAll(id + ' tbody tr');

  for (var i = 0; i < rows.length; i++) {
    var showRow = false;

    var row = rows[i];
    row.style.display = 'none';

    for (var x = 0; x < row.childElementCount; x++) {
      if (row.children[x].textContent.toLowerCase().indexOf(value.toLowerCase().trim()) > -1) {
        showRow = true;
        break;
      }
    }

    if (showRow) {
      row.style.display = null;
    }
  }
}

function selectReclassification(
  id_classification,
  name,
  description,
  existence,
  return_provider
) {
  blockUI("Searching containers");
  $.get(
    "search_container/classification/" + id_classification,
    function (data) {
      containers = data.container;
      console.log(containers);
      $("#reclassification_selected").html("Selected: " + name);
      $("#reclassification_description").html(description);
      $("#info-classification-to-reclassification").show();
      $("#form-reclassification").hide();
      if (existence == 1) {
        $("#form-container-to-reclassification").show();
        $("#container-to-reclassification").focus();
        $("#container-to-reclassification").val("");
      } else {
        container = "WE";
        $("#container").val("Without existence");
      }
      unblockUI();
      validateData();
    }
  );
}

function selecteOtherReclassification() {
  container = "";
  $("#container-to-reclassification").val("");
  $("#containers_info").html("");
  $("#info-classification-to-reclassification").hide();
  $("#form-reclassification").show();
  $("#form-container-to-reclassification").hide();
  $("#message-reclassification").html("");
  validateData();
}

$("#container-to-reclassification").keyup(function (e) {
  if (e.keyCode == 13) {
    $("#message-reclassification").html("");
    var container_val = $("#container-to-reclassification").val();
    var find_container = false;
    var container_lot_week;
    var container_code;
    var return_provider = true;
    var fulfillment_center = "";
    containers.forEach((container) => {
      if (container.code == container_val) {
        find_container = true;
        container_lot_week = container.lot_week;
        container_code = container.code;
        if (container.classification__return_provider == 1) {
          return_provider = true;
        } else {
          return_provider = false;
        }
        fulfillment_center = container.fulfillment_center__fulfillment_center;
      }
    });
    container = "";
    if (find_container) {
      var last_date = $("#last_date").val();
      var lot_week = lootWeek("", last_date);
      if (!return_provider) {
        container = container_code;
        console.log("OK");
      } else {
        if (fulfillment_center == items[item_select].fulfillment_center) {
          container = container_code;
          console.log("OK");
        } else {
          $("#message-reclassification").html(
            "This product does not belong to this fulfillment center."
          );
        }
      }
    } else {
      $("#message-reclassification").html(
        "This container not found in this classification, try other code."
      );
    }
    validateDataReclassification();
  }
});

function validateDataReclassification() {
  if (container != "") {
    $("#save-policy-reclassification").prop("disabled", false);
  } else {
    $("#save-policy-reclassification").prop("disabled", true);
  }
}

$("#save-policy-reclassification").click(function () {
  blockUI("Save policy A");
  $.get("reclassification-in-lot/" + JSON.stringify(items_process) + "/" + container, function (data) {
    container = "";
    if (data.status == 1) {
      $("#fulfillment_center").change();
      selecteOtherReclassification();
      selectContainer(code_container);
      validateDataReclassification();
      $("#modalReClassificationInLot").modal("hide");
      alert_message(data.message);
    }
  });
  unblockUI();
});
