var is_search_tracking = 1;
var items = [];
var item_select = "";
var containers = [];
var sale_order = [];
var items_api = [];
var is_necesary_class_all = true;
var so_fulfillment_center = "";
var so_po_numbers = "";
var so_items = "";
var classification_select = 0;

$("#search_tracking").click(function () {
  is_necesary_class_all = true;
  items = [];
  $("#tbodyProducts").empty();

  var type_search = "tracking";
  let data_search = verify_input_is_null();
  if (data_search[0] != "") {
    blockUI("Searching record");
    $.get("search_tracking/" + data_search[0] + "/" + data_search[1], function (data) {
      if (data.status == 400) {
        no_search_message();
      } else {
        //Datos que se obtienen de la consulta.
        so_order = data.so_order;
        po_order = data.po_order;
        api_info = data.api_elements;
        items_api = api_info.SalesOrder.Items;
        if (data.record) {
          record_info = data.record[0];
        }

        if (data.so_order) {
          if (data.so_order.length != 0) {
            fulfillment_ship_location = so_order.fulfillment_ship_location;
            po_number = so_order.po_numbers
          } else {
            if (data.po_order.length != 0) {
              po_number = "";
              fulfillment_ship_location = "";
              data.po_order.forEach((po) => {
                po_number += " | " + po.po_number;
                fulfillment_ship_location += " | " + po.supplier + " " + po.purchase_locations;
              });
              po_number = po_number.substr(3);
              fulfillment_ship_location = fulfillment_ship_location.substr(3);
            } else {
              po_number = "";
              fulfillment_ship_location = "";
            }
          }
        } else {
          if (data.po_order) {
            if (data.po_order.length != 0) {
              po_number = "";
              fulfillment_ship_location = "";
              data.po_order.forEach((po) => {
                po_number += " | " + po.po_number;
                fulfillment_ship_location += " | " + po.supplier + " " + po.purchase_locations;
              });
              po_number = po_number.substr(3);
              fulfillment_ship_location = fulfillment_ship_location.substr(3);
            } else {
              po_number = "";
              fulfillment_ship_location = "";
            }
          }
          else {
            po_number = "";
            fulfillment_ship_location = "";
          }
        }


        if (data.tracking) {
          if (data.tracking.length != 0) {
            tracking =
              `<strong>Tracking date: </strong> ` +
              tracking_info.date +
              ` <br> <strong>Tracking user: </strong> ` +
              tracking_info.c_user_id;
          } else {
            tracking = `<p style="color:red">Tracking not found</p>`;
          }
        } else {
          tracking = `<p style="color:red">Tracking not found</p>`;
        }

        $("#sale_order_info").html(
          `<label><strong style="font-weight:bold;">Fulfillment center</strong>: <div id="fc_order_return"></div></label><br>
          <label> <strong style="font-weight:bold;">Purchase Order</strong>:<div id="po_order_return"></div></label><br>
          <label> <strong style="font-weight:bold;">SO Number</strong>: <div>` + api_info.SalesOrder.Number + `</div></label><br>
          <label> <strong style="font-weight:bold;">Return Reason:</strong> <div id="return_reason_order_return"></div></label><br>
          <label> <strong style="font-weight:bold;">Total: </strong> <div id="total_order_return"></div></label>`
        );

        return_reason = "";
        total_return = 0.00;
        if (data.record) {
          if (data.record.length != 0) {
            data.record.forEach((element) => {
              console.log(element.order_amount);
              return_reason += " | " + element.return_reason;
              total_return += parseFloat(element.order_amount);
            });
            return_reason = return_reason.substr(3);
          } else {
            return_reason = "";
            total_return = "";
          }
        } else {
          return_reason = "";
          total_return = "";
        }

        $("#return_info").html(
          `<strong style="font-weight:bold;">Address Info</strong>: <hr>` +
          api_info.SalesOrder.ShipTo.FullName +
          `<br>` +
          api_info.SalesOrder.ShipTo.Street1 +
          `<br>` +
          api_info.SalesOrder.ShipTo.City +
          `<br>` +
          api_info.SalesOrder.ShipTo.Postal +
          `<br>` +
          api_info.SalesOrder.ShipTo.StateRegion +
          `<hr> <label><strong style="font-weight:bold;">Fulfillment center</strong>:</label> ` +
          fulfillment_ship_location +
          `<br> <label><strong style="font-weight:bold;">Purchase Order</strong>:</label> ` +
          po_number +
          `<br> <label><strong style="font-weight:bold;">SO Number</strong>:</label> ` +
          api_info.SalesOrder.Number +
          `<br> <label><strong style="font-weight:bold;">Return Reason:</strong> ` +
          return_reason + `</label>
           <br> <label><strong style="font-weight:bold;">Total: </strong> ` +
          total_return + `</label> 
           <br>` + tracking
        );
        let last_date = $("#last_date").val();
        let lot_week = lootWeek("", last_date);

        sale_order = {
          order_id: data_search[0],
          customer_name: api_info.SalesOrder.BillTo.FullName,
          so_number: api_info.SalesOrder.SalesOrderNumber,
          fulfillment_center: "CAR",
          lot_week: lot_week,
        };

        if (data.status == 201) {
          is_necesary_class_all = false;
          api_info.SalesOrder.Items.forEach((item) => {
            evp_sku = item.Sku;
            found_sku = true;

            fulfillment_center_to_add = "";
            po_to_add = "";
            find = false;
            if (po_order.length != undefined) {
              po_order.forEach((element) => {
                element.item_summary.split(' | ').forEach((item) => {
                  if (item.split(" ")[0] == evp_sku) {
                    if (!find) {
                      po_to_add = element.po_number;
                      fulfillment_center_to_add = element.supplier + " " + element.purchase_locations;
                      find = true;
                    }
                  }
                });
              });
            }

            items.push({
              fulfillment_center: fulfillment_center_to_add,
              image: "",
              description: "",
              container: "",
              sku: evp_sku,
              title: item.Title,
              return_quantity: 0,
              order_quantity: item.Shipped * item.UomQuantity,
              quantity: 0,
              quantity_left: item.Shipped * item.UomQuantity,
              totalQuantity: item.Shipped * item.UomQuantity,
              classification: "",
              classification_name: "",
              po_number: po_to_add,
              so_number: api_info.SalesOrder.Number,
              classified: false,
              validated: false,
              found_sku: found_sku,
              is_copy: false,
              total: 0.00,
              return_reason: ""
            });
          });
          loadTableDate();
        } else {
          if (data.in_sale_order == true) {
            unblockUI();
            modal_alert("Record found", "This return has already been classified, please try another package.");
            return;
          }
          var found_sku = false;

          if (record_info.company__id_company == 1) {
            is_necesary_class_all = true;
            data.record.forEach((item) => {
              evp_sku = item.sku;
              found_sku = item.found_sku;
              console.log(found_sku);
              fulfillment_center_to_add = "";
              po_to_add = "";
              find = false;
              if (po_order) {
                if (po_order.length != undefined) {
                  po_order.forEach((element) => {
                    element.item_summary.split(' | ').forEach((item) => {
                      if (item.split(" ")[0] == evp_sku) {
                        if (!find) {
                          po_to_add = element.po_number;
                          fulfillment_center_to_add = element.supplier + " " + element.purchase_locations;
                          find = true;
                        }
                      }
                    });
                  });
                }
              }


              var uomQuantity = 1;
              api_info.SalesOrder.Items.forEach(item_api => {
                if (item_api.Sku == evp_sku) {
                  uomQuantity = item_api.UomQuantity;
                } else {
                  uomQuantity = 1;
                }
              });
              items.push({
                fulfillment_center: fulfillment_center_to_add,
                image: "",
                description: "",
                container: "",
                sku: evp_sku,
                title: item.item_name,
                return_quantity: item.return_quantity * uomQuantity,
                order_quantity: item.order_quantity * uomQuantity,
                quantity: 0,
                quantity_left: item.return_quantity * uomQuantity,
                totalQuantity: item.return_quantity * uomQuantity,
                classification: "",
                classification_name: "",
                po_number: po_to_add,
                so_number: api_info.SalesOrder.Number,
                classified: false,
                validated: false,
                found_sku: found_sku,
                is_copy: false,
                total: item.order_amount / item.return_quantity,
                return_reason: item.return_reason
              });
            });
          } else {
            is_necesary_class_all = false;
            api_info.SalesOrder.Items.forEach((item) => {
              evp_sku = item.Sku;
              found_sku = true;
              fulfillment_center_to_add = "";
              po_to_add = "";
              find = false;
              if (po_order.length != undefined) {
                po_order.forEach((element) => {
                  element.item_summary.split(' | ').forEach((item) => {
                    if (item.split(" ")[0] == evp_sku) {
                      if (!find) {
                        po_to_add = element.po_number;
                        fulfillment_center_to_add = element.supplier + " " + element.purchase_locations;
                        find = true;
                      }
                    }
                  });
                });
              }
              items.push({
                fulfillment_center: fulfillment_center_to_add,
                image: "",
                description: "",
                container: "",
                sku: evp_sku,
                title: item.Title,
                return_quantity: 0,
                order_quantity: item.Shipped * item.UomQuantity,
                quantity: 0,
                quantity_left: item.Shipped * item.UomQuantity,
                totalQuantity: item.Shipped * item.UomQuantity,
                classification: "",
                classification_name: "",
                po_number: po_to_add,
                so_number: api_info.SalesOrder.Number,
                classified: false,
                validated: false,
                found_sku: found_sku,
                is_copy: false,
                total: 0.00,
                return_reason: ""
              });
            });
          }
          loadTableDate();
        }
      }
      unblockUI();
    });
  }
});

function verify_input_is_null() {
  var tracking_id = "";
  if (is_search_tracking == 1) {
    if ($("#tracking_id").val() == "") {
      alert("Please, insert a value in tracking ID");
    }
    type_search = "tracking";
    tracking_id = $("#tracking_id").val();
  } else if (is_search_tracking == 2) {
    if ($("#rma_id").val() == "") {
      alert("Please, insert a value in RMA ID");
    }
    type_search = "rma";
    tracking_id = $("#rma_id").val();
  } else {
    if ($("#so").val() == "") {
      alert("Please, insert a value in sale order");
    }
    type_search = "sale_order";
    tracking_id = $("#so").val();
  }
  return [tracking_id, type_search];
}

function no_search_message() {
  if (is_search_tracking == 1) {
    $("#return_info").html(
      `<p style="color:red">Record not found, try searching by RMA ID</p>`
    );
    $("#search_for_tracking").hide("fast");
    $("#search_for_so").hide("fast");
    $("#search_for_rma").show("fast");
    $("#tracking_id").val("");
    $("#so").val("");
    $("#rma_id").focus();
    is_search_tracking = 2;
  } else if (is_search_tracking == 2) {
    $("#return_info").html(
      `<p style="color:red">Record not found, try searching by sale order</p>`
    );
    $("#search_for_so").show("fast");
    $("#search_for_rma").hide("fast");
    $("#search_for_tracking").hide("fast");
    $("#rma_id").val("");
    $("#tracking_id").val("");
    $("#so").focus();
    is_search_tracking = 3;
  } else {
    $("#return_info").html(`<p style="color:red"> Record not found</p>`);
    $("#search_for_rma").hide("fast");
    $("#search_for_so").hide("fast");
    $("#search_for_tracking").show("fast");
    $("#rma_id").val("");
    $("#so").val("");
    $("#tracking_id").focus();
    is_search_tracking = 1;
  }
}

function openModalManage(no_item) {
  blockUI("Getting information...");
  $("#taken_photo").hide();
  $("#message_taken_photo").hide();
  $(".container_radio").show();
  $("#take_photo").show();
  $("#reset_photo").hide();
  item_select = no_item;
  $.get("search_item_product/" + items[item_select].sku, function (data) {
    $("#quantity").val(items[item_select].quantity_left);
    $("#quantity").attr("max", items[item_select].quantity_left);
    product_info = data.product_info[0];
    var classifications = [];
    var classifications_html = "";
    if (data.product_info.length == 0) {
      unblockUI();
      modal_alert("Product information not found", "No information could be found for the classification of this product, please try another tracking ID.");
      return;
    }
    if (product_info.orm_d == "Unchecked") {
      $.get("get_classification/1", function (data) {
        classifications_list = data.classifications;
        classifications = data.classifications;
        classifications.forEach((cls) => {
          classifications_html =
            classifications_html +
            `<p
          class="btn btn-primary"
          onclick="selectClassification('` +
            cls.id_classification +
            `', '` +
            cls.name +
            `', '` +
            cls.description +
            `', '` +
            cls.existence +
            `', '` +
            cls.return_provider +
            `');" style='margin-left:4px;' 
        >
        ` +
            cls.name +
            `
      </p>`;
        });
        $("#list_classifications").html(classifications_html);
      });

    } else {
      $.get("get_classification/1", function (data) {
        classifications_list = data.classifications;
        classifications = data.classifications;
        classifications.forEach((cls) => {
          classifications_html =
            classifications_html +
            `<p
          class="btn btn-primary"
          onclick="selectClassification('` +
            cls.id_classification +
            `', '` +
            cls.name +
            `', '` +
            cls.description +
            `', '` +
            cls.existence +
            `', '` +
            cls.return_provider +
            `');" style='margin-left:4px;' 
        >
        ` +
            cls.name +
            `
      </p>`;
        });
        $("#list_classifications").html(classifications_html);
      });
    }

    var inactive_reason = "";
    if (product_info.status != "Active") {
      inactive_reason =
        `<br><label><strong>Inactive reason</strong>: ` +
        product_info.inactive_reason +
        `</label>`;
    }
    if (product_info.orm_d == "Checked") {
      var orm = `Yes <i class="fa fa-check" style="color:green;"></i>`;
    } else {
      var orm = `No <i class="fa fa-times" style="color:red;"></i>`;
    }

    var quantity_sale_order = "";
    items_api.forEach(element => {
      if (element.Sku == items[item_select].sku) {
        quantity_sale_order = element.UomQuantity * element.Shipped;
      }
    });

    $("#fc_order_return").html(items[item_select].fulfillment_center);
    $("#po_order_return").html(items[item_select].po_number);
    $("#return_reason_order_return").html(items[item_select].return_reason);
    $("#total_order_return").html(items[item_select].total);
    $("#fulfilment_center_modal").html("<strong style='font-weight:bold;' >Fulfillment center: </strong>" + items[item_select].fulfillment_center);

    $("#product_info").html(
      `<label><strong style="font-weight:bold;">SKU</strong>: ` +
      product_info.master_sku +
      `</label><br><label><strong style="font-weight:bold;">Status</strong>: ` +
      product_info.status +
      `</label>` +
      inactive_reason +
      `<br> <label><strong style="font-weight:bold;">Title</strong>:` +
      product_info.title +
      `</label><br> <label><strong style="font-weight:bold;">Manufacturer</strong>: ` +
      product_info.manufacturer +
      `</label><br> <label><strong style="font-weight:bold;">Part</strong>: ` +
      product_info.part +
      `</label><br><label><strong style="font-weight:bold;">UPC</strong>: ` +
      product_info.upc +
      `</label><br> <label><strong style="font-weight:bold;">ORM D</strong>: ` +
      orm +
      `</label><br> <label><strong style="font-weight:bold;">Created date</strong>: ` +
      product_info.created_date +
      `</label><br> <label><strong style="font-weight:bold;">Quantity in sale order</strong>: ` +
      quantity_sale_order
    );

    if (data.url_image != "") {
      $("#image_product").show();
      $("#img_not_found").hide();
      $("#image_product").attr("src", data.url_image);
    } else {
      $("#image_product").hide();
      $("#img_not_found").show();

    }
    $("#image_product").attr("src", data.url_image);
    $("#description").val("");
    $("#form-container").hide();
    $("#container").val("");
    $("#modalManage").modal("show");
    validateData();
    selecteOther();
    unblockUI();
  });
}

$("body").on("shown.bs.modal", "#modalManage", function () {
  $("#description", this).focus();
});

function selectClassification(
  id_classification,
  name,
  description,
  existence,
  return_provider
) {
  classification_select = id_classification;
  blockUI("Searching containers");
  $.get(
    "search_container/classification/" + id_classification,
    function (data) {
      containers = data.container;
      items[item_select].classification = id_classification;
      items[item_select].classification_name = name;
      if (return_provider == "1") {
        $("#description").val("Good condition");
      } else {
        var good_condition = "Good condition";
        var descr = $("#description").val();
        if (descr.toString() == good_condition.toString()) {
          $("#description").val("");
        }
      }
      $("#classification_selected").html(name);
      $("#classification_description").html(description);
      $("#info-classification").show();
      $("#form-classification").hide();
      if (existence == 1) {
        $("#form-container").show();
        if (return_provider == "1") {
          $("#description").val("Good condition");
          $("#description").keyup();
          $("#description").focus();
          $("#container").focus();
        } else {
          var good_condition = "Good condition";
          var descr = $("#description").val();
          if (descr.toString() == good_condition.toString()) {
            $("#description").val("");
          }
        }
        $("#description").keyup();
        $("#description").focus();
        //$("#container").focus();
        $("#container").val("");
      } else {
        items[item_select].container = "WE";
        $("#container").val("Without existence");
      }
      if (name == "Missing") {
        $("#description").val("Missing");
        $("#description").keyup();
        $("#description").focus();
      }
      var containers_info = "<strong style='font-weight:bold;'>Container suggestion :</strong> <br>";
      containers.forEach((element) => {
        containers_info = containers_info + `<a href="#" onclick='selectCodeContainer("` + element.code + `");'>` + element.code + `</a>` + `<br>`;
      });
      if (return_provider == "2" && existence == "1") {
        $("#containers_info").html(containers_info);
      }
      unblockUI();
      validateData();
    }
  );
}

function selectCodeContainer(code) {
  $("#container").val(code);
  $("#container").focus();
  insert_container();
}

function selecteOther() {
  $("#containers_info").html("");
  items[item_select].container = "";
  items[item_select].classification = "";
  $("#info-classification").hide();
  $("#form-classification").show();
  $("#form-container").hide();
  $("#message").html("");
  validateData();
}

$("#description").keyup(function () {
  items[item_select].description = $("#description").val();
  validateData();
});

$(".openModalManage").click(function () {
  $("#modalManage").modal("show");
});

function take_photo() {
  if (checkCamera()) {
    cxt.drawImage(video, 0, 0, 300, 150);
    var data = canvas.toDataURL("image/jpeg");
    var info = data.split(",", 2);
    items[item_select].image = info;
    $("#taken_photo").attr("src", items[item_select].image[0] + "," + items[item_select].image[1]);
    $("#taken_photo").show();
    $(".container_radio").hide();
    //$("#message_taken_photo").show();
    $("#take_photo").hide();
    $("#reset_photo").show();
    validateData();
  } else {
    alert("A problem occurred while trying to take the photo.");
  }
}

function reset_photo() {
  $(".container_radio").show();
  $("#taken_photo").hide();
  $("#take_photo").show();
  $("#reset_photo").hide();
}

$("#save-manage").click(function () {
  if (items[item_select].validated != false) {
    items[item_select].quantity = parseInt($("#quantity").val());
    items[item_select].quantity_left -= $("#quantity").val();
    if (items[item_select].quantity_left != 0) {
      items.splice(item_select + 1, 0, {
        fulfillment_center: "CAR",
        description: "",
        container: "",
        sku: items[item_select].sku,
        title: items[item_select].title,
        return_quantity: items[item_select].return_quantity,
        order_quantity: items[item_select].order_quantity,
        quantity: 0,
        quantity_left: items[item_select].quantity_left,
        totalQuantity: items[item_select].quantity_left,
        classification: "",
        classification_name: "",
        po_number: items[item_select].po_number,
        so_number: items[item_select].so_number,
        classified: false,
        validated: false,
        found_sku: items[item_select].found_sku,
        is_copy: true,
        total: items[item_select].total,
        return_reason: items[item_select].return_reason
      });
    }
    items[item_select].classified = true;
    loadTableDate();

    $("#modalManage").modal("hide");
  } else {
    alert("Missing information to validate.");
  }
  validateItems();
});

function loadTableDate() {
  $("#tbodyProducts").empty();
  var cont = 0;
  items.forEach((item) => {
    if (item.quantity == 0) {
      var quantity = item.totalQuantity;
    } else {
      var quantity = item.quantity;
    }
    if (item.classification_name == "") {
      if (!item.found_sku) {
        var classification_name = "SKU not found";
      } else {
        var classification_name = "Unclassified";
      }
    } else {
      var classification_name = item.classification_name;
    }

    var f_c = item.sku.substr(0, 3);
    var url_image = "<i class='fas fa-image fa-3x'><i>";
    if (f_c == "ACE") {
      url_image =
        "<image width='50px' height='50px' src='https://unauthimages.aceservices.com/" +
        item.sku.substr(4, 2) +
        "/" +
        item.sku.substr(6, 2) +
        "/" +
        item.sku.substr(4, 7) +
        "_A.eps_High.jpg' alt='Image product'>";
    }
    if (f_c == "EJD") {
      url_image =
        "<image width='50px' height='50px' src='https://unauthimages.aceservices.com/" +
        item.sku.substr(4, 2) +
        "/" +
        item.sku.substr(6, 2) +
        "/" +
        item.sku.substr(4, 7) +
        "_A.eps_High.jpg' alt='Image product'>";
    }
    if (f_c == "JEN") {
      url_image =
        "<image width='50px' height='50px' src='http://www.jensenonline.com/cares/webimages/" +
        item.sku.substr(4, 4) +
        "" +
        item.sku.substr(9, 4) +
        "c.jpg' alt='Image product'>";
      url_image = "<i class='fas fa-image fa-3x'><i>";
    }
    var button_action = "";
    if (item.classified) {
      if (!item.is_copy) {
        button_action = '<button class="btn btn-primary openModalManage" onclick="restart(' + cont + ')";>Restart</button>';
      } else {
        button_action = '<button class="btn btn-primary openModalManage" disabled onclick="openModalManage(' + cont + ')";>Manage</button>';
      }
    } else {
      if (item.found_sku) {
        button_action = '<button class="btn btn-primary openModalManage" onclick="openModalManage(' + cont + ')";>Manage</button>';
      } else {
        button_action = '<button class="btn btn-primary openModalManage" disabled onclick="openModalManage(' + cont + ')";>Manage</button>';
      }
    }
    $("#table_products").append(
      "<tr><td>" +
      url_image +
      "</td><td>" +
      item.sku +
      " <br> " +
      item.title +
      "</td><td>" +
      item.order_quantity +
      "</td><td>" +
      item.return_quantity +
      "</td><td>" +
      quantity +
      '</td><td id="classified_' +
      cont +
      '">' +
      classification_name +
      "</td><td>" + button_action + "</td></tr>"
    );
    cont++;
  });
}

function restart(no_item) {
  blockUI("Getting information...");
  item_select = no_item;
  sku = items[item_select].sku;
  var cont = 0;
  var items_delete = [];
  items.forEach(item => {
    if (item.sku == sku && item.is_copy) {
      items_delete.push(cont);
    }
    cont++;
  });
  var cont_delete = 0;
  items_delete.forEach(id => {
    items.splice(id - cont_delete, 1);
    cont_delete++
  });
  items[item_select].quantity = 0;
  items[item_select].classified = false;
  items[item_select].validated = false;
  items[item_select].classification_name = "";
  items[item_select].quantity_left = parseInt(items[item_select].totalQuantity);
  unblockUI();
  loadTableDate();
  validateItems();
}

$("#tracking_id").keyup(function (e) {
  if (e.keyCode == 13) {
    $("#search_tracking").click();
  }
});

$("#rma_id").keyup(function (e) {
  if (e.keyCode == 13) {
    $("#search_tracking").click();
  }
});

$("#so").keyup(function (e) {
  if (e.keyCode == 13) {
    $("#search_tracking").click();
  }
});

$("#container").keyup(function (e) {
  if (e.keyCode == 13) {
    insert_container();
  }
});

function insert_container() {
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
  if (find_container) {
    var last_date = $("#last_date").val();
    var lot_week = lootWeek("", last_date);

    if (container_lot_week == lot_week || classification_select != 1) {
      items[item_select].container = container_code;
    } else {
      $("#message").html("The lot week is not correct, try other code.");
    }
  } else {
    $("#message").html(
      "This container not found in this classification, try other code."
    );
  }
  validateData();
}

function validateData() {
  if (
    items[item_select].description != "" &&
    items[item_select].container != "" &&
    items[item_select].classification != "" &&
    items[item_select].image != ""
  ) {
    items[item_select].validated = true;
    $("#save-manage").prop("disabled", false);
  } else {
    items[item_select].validated = false;
    $("#save-manage").prop("disabled", true);
  }
}

function validateItems() {
  var allValidated = true;
  if (is_necesary_class_all) {
    items.forEach((item) => {
      if (!item.classified) {
        allValidated = false;
      }
    });
  } else {
    allValidated = false;
    items.forEach((item) => {
      if (item.classified) {
        allValidated = true;
      }
    });
  }

  if (allValidated) {
    $("#send-ticket").prop("disabled", false);
  } else {
    $("#send-ticket").prop("disabled", true);
  }
}

$("#send-ticket").click(function () {
  blockUI("Save data and send mail");
  $("#sale_order").val(JSON.stringify(sale_order));
  $("#items").val(JSON.stringify(items));
  $("#sale_order_form").submit();
});
