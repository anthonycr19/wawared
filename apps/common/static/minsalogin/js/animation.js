var hover = function () {
  $('.post-module').hover(function () {
    $(this).find('.description').stop().animate({
      height: "toggle",
      opacity: "toggle"
    }, 300);
  });
};
var rescreen = function () {
  screenObj = screen.width;
  if (screenObj < 416) {
    $("#menu-toggle-2").click(function (e) {
      $("#sidebar-wrapper").toggleClass("toggled-2");
      $(".modulo").removeClass("ocultar");
      $(".modulo").toggleClass("block");
    });
  }
  else {
    console.log('Nice!')
  }
};
$(document).ready(function () {
  var heightBottom = $(".menu-bottom").height();
  if (heightBottom <= 80) {
    $(".menu-bottom").addClass("newBottom2");
  }
  hover();
  rescreen();
  var activos = $(".menu-content li");
  $(activos).click(function () {
    activos.removeClass("active");
    $(this).addClass("active");
  });
  $("#aparecer").toggleClass("hidden");
  $("#contentIconLupa").click(function () {
    $(".buscadorDiv").slideToggle();
    $(".mi-slider").toggleClass("opacity");
  });
  $("#menu-toggle-2").click(function (e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled-2");
    $(".flechaMenuDespl").toggleClass("ocultar");
    $(".modulo").toggleClass("ocultar");
    $("#menu-content ul").toggleClass("collapsing");
    $(".nameHospitalSidebar").toggleClass("ocultar");
  });
  $("#buscadorBoton").click(function () {
    var resultado = $(".resultadoBusqueda");
    var formBuscador = $(".formBuscador");
    resultado.removeClass("ocultar");
    formBuscador.addClass("ocultar");
  });
  $(".active").click(function () {
    var heightBottom = $(".menu-bottom").height();
    if (heightBottom > 350) {
      $(".menu-list").toggleClass("newList2");
    }
    else if (heightBottom < 300) {

      $(".menu-list").toggleClass("newList2");
    }
  });
});
