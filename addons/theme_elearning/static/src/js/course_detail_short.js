$(".item").click(function () {
  $(".item").removeClass("active");
  $(this).addClass("active");
  // Cập nhật tên giáo viên trên giao diện
  updateTeacher();
  updateLocation();
});

function updateLocation() {
  let activeLocation = $(".item.active").text().trim();

  // Kiểm tra nếu là Remote Teaching thì hiển thị text đặc biệt
  let locationText =
    activeLocation === "Remote Teaching"
      ? "Học trực tuyến với giảng viên qua Zoom/ Meet/ Classin..."
      : activeLocation;

  // Cập nhật nội dung hiển thị
  $(".location-text").text(locationText);
}

function updateTeacher() {
  // Cập nhật tên giáo viên lên giao diện
  let teacherName = $(".item.active").data("teacher") || "Chưa có giáo viên";

  $(".course-info .teacher-name").text(teacherName);
}

updateTeacher();
updateLocation();

$(".subnav ul li").click(function () {
  $("li").removeClass("active");
  $(this).addClass("active");
});

$("li .title").click(function () {
  var lesson = $(this).next(".lesson");
  var icon = $(this).find("i");

  if (lesson.is(":visible")) {
    lesson.slideUp();
    icon.removeClass("fa-minus").addClass("fa-plus");
  } else {
    lesson.slideDown();
    icon.removeClass("fa-plus").addClass("fa-minus");
  }
});
