function makeChart (url, elem) {
    function drawResume (data) {
        Raphael.fn.line = function (x1, y1, x2, y2) {
            return this.path('M' + x1 + ' ' + y1 + ' L' + x2 + ' ' + y2);
        };
        var paper = new Raphael(elem, 1000, 300);
        var rectanglesCoordinates = [
            {
                x: 10,
                y: 10,
                name: 'Gestas',
                value: data.gestas
            },
            {
                x: 200,
                y: 10,
                name: 'Abortos',
                value: data.abortos
            },
            {
                x: 200,
                y: 100,
                name: 'Partos',
                value: data.partos
            },
            {
                x: 400,
                y: 10,
                name: 'Vaginales',
                value: data.vaginales
            },
            {
                x: 400,
                y: 100,
                name: 'Cesáreas',
                value: data.cesareas
            },
            {
                x: 600,
                y: 10,
                name: 'Nacidos\nVivos',
                value: data.nacidos_vivos
            },
            {
                x: 600,
                y: 100,
                name: 'Nacidos\nMuertos',
                value: data.nacidos_muertos
            },
            {
                x: 800,
                y: 10,
                name: 'Viven',
                value: data.viven
            },
            {
                x: 800,
                y: 100,
                name: 'Muerto - 1ra\nsemana',
                value: data.muerto_primera_semana
            },
            {
                x: 800,
                y: 200,
                name: 'Después - 1ra\nsemana',
                value: data.muerto_despues_primera_semana
            }
        ];
        var i;
        // rectangles
        var rectWidth = 50;
        var rectHeight = 30;
        for (i=0; i<rectanglesCoordinates.length; i++) {
            var item = rectanglesCoordinates[i];
            var rect = paper.rect(item.x, item.y, rectWidth, rectHeight, 5);
            rect.attr('stroke', '#000');
            rect.attr('fill', '#FFF');
            var value = paper.text(item.x + (rectWidth / 2), item.y + (rectHeight / 2), item.value);
            value.attr('font-size', '16px');
            var valueY = item.y + rectWidth;
            if (item.name.indexOf('\n') === -1) {
                valueY -= 10;

            }
            var text = paper.text(item.x + (rectWidth / 2), valueY, item.name);
            text.attr('font-size', '14px');
        }
        var rect = paper.rect(395, 245, rectWidth + 160, rectHeight, 5);
        var text = paper.text(500 , 260 , "R.N Mayor peso : "+ data.mayor_peso + " gr");
        text.attr('font-size', '18px');
        // lines
        paper.line(10 + rectWidth, 10 + (rectHeight / 2), 200, 10 + (rectHeight / 2));
        paper.line(10 + rectWidth, 10 + (rectHeight / 2), 200, 100 + (rectHeight / 2));
        paper.line(200 + rectWidth, 100 + (rectHeight / 2), 400, 10 + (rectHeight / 2));
        paper.line(200 + rectWidth, 100 + (rectHeight / 2), 400, 100 + (rectHeight / 2));
        paper.line(400 + rectWidth, 10 + (rectHeight / 2), 400 + rectWidth + 50, 10 + (rectHeight / 2));
        paper.line(400 + rectWidth, 100 + (rectHeight / 2), 400 + rectWidth + 50, 100 + (rectHeight / 2));
        paper.line(400 + rectWidth + 50, 10 + (rectHeight / 2), 400 + rectWidth + 50, 100 + (rectHeight / 2));
        paper.line(500, 50 + (rectHeight / 2), 600, 10 + (rectHeight / 2));
        paper.line(500, 50 + (rectHeight / 2), 600, 100 + (rectHeight / 2));
        paper.line(600 + rectWidth, 10 + (rectHeight / 2), 800, 10 + (rectHeight / 2));
        paper.line(600 + rectWidth, 10 + (rectHeight / 2), 800, 100 + (rectHeight / 2));
        paper.line(600 + rectWidth, 10 + (rectHeight / 2), 800, 200 + (rectHeight / 2));
        // squares
        var squaresCoordinates = [
            {
                x: 100,
                y: 100,
                name: '0 ó + 3',
                value: data.cero_o_mas_3
            },
            {
                x: 100,
                y: 130,
                name: '< 2500g',
                value: data.menor_2500_g
            },
            {
                x: 100,
                y: 160,
                name: 'Múltiple',
                value: data.multiple
            },
            {
                x: 100,
                y: 190,
                name: '< 37 sem',
                value: data.menor_37_sem
            }
        ];
        var squareSide = 20;
        for (i=0; i<squaresCoordinates.length; i++) {
            item = squaresCoordinates[i];
            var square = paper.rect(item.x, item.y, squareSide, squareSide);
            text = paper.text(item.x - 50, item.y + 10, item.name);
            text.attr('font-size', '12px');
            value = paper.text(item.x + (squareSide / 2), item.y + (squareSide/ 2), item.value);
            value.attr('font-size', '12px');
        }
    }
    $.getJSON(url, function (data) {
        drawResume(data);
    });
}