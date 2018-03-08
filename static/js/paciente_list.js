$(document).ready(function () {

    var env = false;

    $('html').on('click', 'a.beforeclick', function (event) {
        if (env) {
            $('a').attr("href", "javascript:void(0)");
        }

        env = true;
    });

    $("#btn_registrar_ges").hide();

    var t = $_GET("t");
    var q = $_GET("q");
    var q2 = $_GET("q2");

    if (t) {
        $("#tipo_busqueda_paciente").val(t);
        $_mostrar_campos_x_opcion(t);

        $("#q").val(q);

        if (q2) {
            $("#q2").val(q2);
        }

        if (t != "1") {
            $("#btn_registrar_ges").show();
        }

    }


    $("#tipo_busqueda_paciente").change(function () {

        var opcion = $("#tipo_busqueda_paciente").val();

        $_mostrar_campos_x_opcion(opcion);

    });

    function $_GET(param) {
        /* Obtener la url completa */
        url = document.URL;
        /* Buscar a partir del signo de interrogación ? */
        url = String(url.match(/\?+.+/));
        /* limpiar la cadena quitándole el signo ? */
        url = url.replace("?", "");
        /* Crear un array con parametro=valor */
        url = url.split("&");

        /*
         Recorrer el array url
         obtener el valor y dividirlo en dos partes a través del signo =
         0 = parametro
         1 = valor
         Si el parámetro existe devolver su valor
         */
        x = 0;
        while (x < url.length) {
            p = url[x].split("=");
            if (p[0] == param) {
                return decodeURIComponent(p[1]);
            }
            x++;
        }
    }

    function $_mostrar_campos_x_opcion(opcion) {
        if (opcion == 1) {
            var vhtml = "<input type=\"number\" id=\"q\" name=\"q\" class=\"form-control\" placeholder=\"DNI\" autofocus>" +
                "        <span class=\"input-group-addon\">" +
                "            <button>" +
                "                <span class=\"glyphicon glyphicon-search\"></span>" +
                "            </button>" +
                "        </span>";
            $("#id_campos").html(vhtml);
            $("#q").focus();
        }

        if (opcion == 2) {
            var vhtml = "<div class=\"col-sm-6\">" +
                "<input type=\"text\" id=\"q2\" name=\"q2\" class=\"form-control\" placeholder=\"Apellidos\" autofocus>" +
                "</div>" +
                "<div class=\"col-sm-6\">" +
                "<input type=\"text\" id=\"q\" name=\"q\" class=\"form-control\" placeholder=\"Nombres\" autofocus>" +
                "</div>" +
                "        <span class=\"input-group-addon\">" +
                "            <button>" +
                "                <span class=\"glyphicon glyphicon-search\"></span>" +
                "            </button>" +
                "        </span>";
            $("#id_campos").html(vhtml);
            $("#q2").focus();
        }

        if (opcion == 3) {
            var vhtml = "<input type=\"text\" id=\"q\" name=\"q\" class=\"form-control\" placeholder=\"Otro Documento\" autofocus>" +
                "        <span class=\"input-group-addon\">" +
                "            <button>" +
                "                <span class=\"glyphicon glyphicon-search\"></span>" +
                "            </button>" +
                "        </span>";
            $("#id_campos").html(vhtml);
            $("#q").focus();
        }
    }
});
