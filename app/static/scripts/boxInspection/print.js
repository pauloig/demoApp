$(document).ready(function () {
  var code = $("#code").val();
  JsBarcode("#barcode", code, {
    width: 3,
    height: 100,
    fontSize: 50,
    displayValue: true,
  });

  window.print();

  window.open("", "_parent", "");

  //window.close();
});
