$(document).ready(function () {
  $("#captureBtn").click(function () {
    var element_id = $("#element_id").val();
    var design_id = $("#design_id").val();
    var color = $("#color").val();

    if (!element_id || !design_id || !color) {
      alert("Please fill in all fields");
      return;
    }

    $.ajax({
      url: "/capture",
      method: "POST",
      data: {
        element_id: element_id,
        design_id: design_id,
        color: color,
      },
      success: function (response) {
        $("#cam0-image").html(`
          <h3>Camera 0 Image</h3>
          <img src="${response.cam0_image}" alt="Camera 0 Image">
        `);
        $("#cam1-image").html(`
          <h3>Camera 1 Image</h3>
          <img src="${response.cam1_image}" alt="Camera 1 Image">
        `);
      },
      error: function () {
        alert("Error capturing images");
      },
    });
  });
});
