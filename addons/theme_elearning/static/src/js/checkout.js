$('input[name="checkout_with"]').on("change", function () {
  // Ẩn tất cả các form trước khi hiển thị cái được chọn
  $("#checkoutWithLoginForm, #checkoutWithRegisterForm").addClass("d-none");

  // Hiển thị form tương ứng với radio được chọn
  if ($(this).attr("id") === "checkoutWithLogin") {
    $("#checkoutWithLoginForm").removeClass("d-none");
  } else if ($(this).attr("id") === "checkoutWithRegister") {
    $("#checkoutWithRegisterForm").removeClass("d-none");
  }
});
