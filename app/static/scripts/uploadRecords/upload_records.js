import TableCSV from "../TableCSV.js";

const tableRoot = document.querySelector("#csvRoot");
const csvFileInput = document.querySelector("#file");
const tableCsv = new TableCSV(tableRoot);
var delimiter = "\t";

$("#company").change(function(){
  var company = $("#company").val();
  if(company == 1){
    delimiter = "\t";
  }else if(company == 2){
    delimiter = ";"
  }
});

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
    delimiter: delimiter,
    skipEmptyLines: true,
    complete: (results) => {
      $("#no_files").html("Total records: " + results.data.slice(1).length);
      tableCsv.update(results.data.slice(1, 3), results.data[0]);
    },
  });
});

$("#save-button-records").click(function () {
  if ($("#file").val() != "") {
    blockUI("Upload info");
  }
  $(".save-submit").click();
});
