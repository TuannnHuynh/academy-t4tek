$(".item").click(function () {
  $(".item").removeClass("active");
  $(this).addClass("active");
});

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
