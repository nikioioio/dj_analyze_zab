anychart.onDocumentReady(function () {

    var stage = anychart.graphics.create("container");


    chart1 = get_pie_chart();
    chart2 = get_histogram_chart();
    chart2.listen('pointsSelect', draw_details)
    // set container id for the chart

    chart1.bounds(0, 0, "50%", "70%");
    chart2.bounds("50%", 0, "50%", "70%");

    chart1.container(stage);
    chart1.draw();
    chart2.container(stage);
    chart2.draw();
    chart2.getSeries(0).select(0);
    draw_details();
});

function draw_details() {

    points = chart2.getSelectedPoints();
    for (i = 0; i < points.length; i++) {
        // chart1.line(points[i].get('detail')).name(points[i].get('x'));
        chart1.data(points[i].get('detail')).title(points[i].get('x'))
    }
    ;
}

function get_pie_chart() {
    // create pie chart with passed data
    var chart = anychart.pie();
    chart.background().stroke({
        color: "grey"
    });
    chart.animation(true);
    // set chart title text settings
    chart
        .title('ACME Corp. apparel sales through different retail channels')
        // create empty area in pie chart
        .innerRadius('40%');

    // set chart labels position to outside
    chart.labels().position('outside');

    chart.background().fill({
        opacity: "0.0",
        mode: "fit"
    });

    return chart
}

function get_histogram_chart() {
    var chart = anychart.bar();

    chart.background().stroke({
        color: "grey"
    });

    chart.animation(true);

    chart.padding([10, 40, 5, 20]);

    chart.title('Top 10 Cosmetic Products by Revenue');

    // create bar series with passed data
    var series = chart.bar([
        {
            x: 'Eyeshadows',
            value: 249980,
            detail: [['Department Stores', 6371664], ['Discount Stores', 7216301], ['Men\'s/Women\'s Stores', 1486621], ['Juvenile Specialty Stores', 786622], ['All other outlets', 900000]]
        },
        {
            x: 'Eyeshadow1',
            value: 2499810,
            detail: [['Department Stores', 855], ['Discount Stores', 955], ['Men\'s/Women\'s Stores', 1000], ['Juvenile Specialty Stores', 80484], ['All other outlets', 59495]]
        },
        {
            x: 'Eyeshadow2',
            value: 85200,
            detail: [['Department Stores', 85464], ['Discount Stores', 5465], ['Men\'s/Women\'s Stores', 456], ['Juvenile Specialty Stores', 80484], ['All other outlets', 59495]]
        }
    ]);

    // set tooltip settings
    series
        .tooltip()
        .position('right')
        .anchor('left-center')
        .offsetX(5)
        .offsetY(0)
        .titleFormat('{%X}')
        .format('${%Value}');

    // set yAxis labels formatter
    chart.yAxis().labels().format('{%Value}{groupsSeparator: }');

    // set titles for axises
    chart.xAxis().title('Products by Revenue');
    chart.yAxis().title('Revenue in Dollars');
    chart.interactivity().hoverMode('by-x');
    chart.tooltip().positionMode('point');
    // set scale minimum
    chart.yScale().minimum(0);
    chart.background().fill({
        opacity: "0.0",
        mode: "fit"
    });
    return chart
}



