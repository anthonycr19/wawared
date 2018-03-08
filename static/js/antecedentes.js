$(document).ready(function () {
    $('input[type=text]').addClass('form-control');
    var $fechaUltimoPAP = $('#id_fecha_ultimo_papanicolaou');
    var $fechaUltimoPAPPicker = $fechaUltimoPAP.datepicker({
        onRender: function (date) {
            return date.valueOf() > (new Date).valueOf() ? 'disabled' : '';
        }
    });
    var $resultadoPAP = $('#id_resultado_papanicolaou');
    var $lugarPAP = $('#id_lugar_papanicolaou');
    var $tienePAP = $('form input[name=tiene_papanicolaou]');
    var $ningunAnticonceptivo = $('#ningun-metodo-anticonceptivo');
    var $regimenRegular = $('#id_regimen_regular');
    var $duracionMenstruacion = $('#id_duracion_menstruacion');
    var $cicloMenstruacion = $('#id_ciclo_menstruacion');
    var $edadMenarquia = $('#id_edad_menarquia');
    var $edadPrimeraRelacionSexual = $('#id_edad_primera_relacion_sexual');
    var edadActual = paciente_edad;
    var $antitetanicaValor = $('.antitetanica-valor');
    var $falseNoneRadio = $('.false-none-radio');
    var $numeroDosisPrevias = $('#id_antitetanica_numero_dosis_previas');
    var $papObservacion = $('#id_pap_observacion');

    var validator = $('#form-antecedentes').validate({
        errorClass: "alert alert-danger",
        errorElement: "div"
    });

    $numeroDosisPrevias.addClass("antitetanica_numero_dosis_previas")
        .on('focusout', function () {
            validator.element('#id_antitetanica_numero_dosis_previas');
        });
    $('#id_antitetanica_primera_dosis_valor')
        .addClass("antitetanica_primera_dosis_valor")
        .on('focusout', function () {
            validator.element('#id_antitetanica_primera_dosis_valor');
        });
    $('#id_antitetanica_segunda_dosis_valor')
        .addClass("antitetanica_segunda_dosis_valor")
        .on('focusout', function () {
            validator.element('#id_antitetanica_segunda_dosis_valor');
        });
    $('#id_antitetanica_tercera_dosis_valor')
        .addClass("antitetanica_tercera_dosis_valor")
        .on('focusout', function () {
            validator.element('#id_antitetanica_tercera_dosis_valor');
        });

    $.validator.addMethod('enterospositivos', function (value) {
        return /^\d*$/.test(value);
    }, 'Por favor ingrese valores positivos');

    $.validator.addClassRules({
        antitetanica_numero_dosis_previas: {
            enterospositivos: true,
        },
        antitetanica_primera_dosis_valor: {
            enterospositivos: true,
        },
        antitetanica_segunda_dosis_valor: {
            enterospositivos: true,
        },
        antitetanica_tercera_dosis_valor: {
            enterospositivos: true,
        },
    });

    if ($numeroDosisPrevias.val() === '') {
        $numeroDosisPrevias.val('0');
    }
    function validatePAP(bool) {
        if (bool) {
            $lugarPAP.attr('readOnly', false);
            $resultadoPAP.attr('readOnly', false);
            $fechaUltimoPAP.attr('readOnly', false);
        } else {
            $lugarPAP.attr('readOnly', true);
            $resultadoPAP.attr('readOnly', true);
            $fechaUltimoPAP.attr('readOnly', true);
        }
    }

    function validatePapResultado(value) {
        if (value === 'anormal') {
            $papObservacion.parents('.form-group').show();
        } else {
            $papObservacion.parents('.form-group').hide();
        }
    }

    validatePapResultado($resultadoPAP.val());

    $resultadoPAP.on('change', function () {
        validatePapResultado(this.value);
    });

    validatePAP($tienePAP.eq(0).is(':checked'));
    $fechaUltimoPAPPicker.on('changeDate', function () {
        $fechaUltimoPAPPicker.datepicker('hide');
    });
    $tienePAP.on('change', function () {
        validatePAP($tienePAP.eq(0).is(':checked'));
    });

    var $checboxMac = $('.checkbox.mac').find('input');

    $ningunAnticonceptivo.on('change', function () {
        if ($ningunAnticonceptivo.is(':checked')) {
            $checboxMac.prop('checked', false);
        }
    });
    $checboxMac.on('change', function () {
        if ($(this).is(':checked')) {
            $ningunAnticonceptivo.prop('checked', false);
        }
    })
    // validate number only
    var arrowKeys = [37, 38, 39, 40];

    function validateOnlyNumber(event) {
        if (arrowKeys.indexOf(event.keyCode) === -1) {
            this.value = this.value.replace(/[^0-9\.]/g, '');
        }
    }

    function validate3Digits(event) {
        if (arrowKeys.indexOf(event.keyCode) === -1) {
            this.value = this.value.replace(/[^0-9\.]/g, '');
            this.value = this.value.substring(0, 3);
        }
    }

    function validateLessThanCurrentAge(event) {
        if (arrowKeys.indexOf(event.keyCode) === -1) {
            this.value = this.value.replace(/[^0-9\.]/g, '');
            this.value = this.value <= edadActual ? this.value : '';
        }
    }

    $antitetanicaValor.find('input[type=text]').on('keyup', function (event) {
        if (arrowKeys.indexOf(event.keyCode) === -1) {
            this.value = this.value.replace(/[^0-9\.]/g, '');
            this.value = this.value.substring(0, 1);
            if (this.value.length) {
                $(this).parents('tr').find('input[type=radio][value="True"]').prop('checked', true);
            } else {
                $(this).parents('tr').find('input[type=radio][value="None"]').prop('checked', true);
            }
        }
    });
    $falseNoneRadio.on('change', function () {
        if ($(this).is(':checked')) {
            $(this).parents('tr').find('input[type=text]').val('');
        }
    });
    $numeroDosisPrevias.on('keyup', validateOnlyNumber);
    $('#id_andria').on('keyup', validateOnlyNumber);
    $edadMenarquia.on('keyup', validateLessThanCurrentAge);
    $edadPrimeraRelacionSexual.on('keyup', validateLessThanCurrentAge);
    $duracionMenstruacion.on('keyup', validate3Digits);
    $cicloMenstruacion.on('keyup', validate3Digits);

    function checkRegimen() {
        if ($regimenRegular.is(':checked')) {
            $duracionMenstruacion.attr('readOnly', false);
            $cicloMenstruacion.attr('readOnly', false);
        } else {
            $duracionMenstruacion.attr('readOnly', true);
            $cicloMenstruacion.attr('readOnly', true);
        }
    }

    checkRegimen();
    $regimenRegular.on('change', checkRegimen);
    makeChart(url_antedentes, 'resume-div');
});
