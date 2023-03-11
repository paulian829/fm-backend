(function ($) {
    "use strict";

    $.ajax({
        url: '/render-chart',
        type: 'GET',
        dataType: 'json',
        success: function(response) {
            let data = response;
            console.log(response); // Outputs the JSON array of past 12 days to the console
            var optionscolumnchart = {
                series: [{
                    name: 'Captured Images',
                    data: data.images_per_day}],
                // }, {
                //     name: 'Revenue',
                //     data: [76, 85, 101, 98, 87, 105, 91, 114, 94]
                // }, {
                //     name: 'Free Cash Flow',
                //     data: [35, 41, 36, 26, 45, 48, 52, 53, 41]
                // }],
        
                legend: {
                    show: false
                },
                chart: {
                    type: 'bar',
                    height: 380
                },
                plotOptions: {
                    bar: {
                        radius: 10,
                        horizontal: false,
                        columnWidth: '55%',
                    }
                },
                dataLabels: {
                    enabled: false
                },
                stroke: {
                    show: true,
                    colors: ['transparent'],
                    curve: 'smooth',
                    lineCap: 'butt'
                },
                grid: {
                    show: false,
                    padding: {
                        left: 0,
                        right: 0
                    }
                },
                xaxis: {
                    categories: data.past_12_days,
                },
                yaxis: {
                    title: {
                        text: '$ (images)'
                    }
                },
                fill: {
                    colors: [cubaAdminConfig.primary, cubaAdminConfig.secondary, '#51bb25'],
                    type: 'gradient',
                    gradient: {
                        shade: 'light',
                        type: 'vertical',
                        shadeIntensity: 0.1,
                        inverseColors: false,
                        opacityFrom: 1,
                        opacityTo: 0.9,
                        stops: [0, 100]
                    }
                },
        
                tooltip: {
                    y: {
                        formatter: function (val) {
                            return " " + val + " images"
                        }
                    }
                }
            };
        
        
        
            var chartcolumnchart = new ApexCharts(
                document.querySelector("#chart-widget4"),
                optionscolumnchart
            );
            chartcolumnchart.render();
        
        
        },
        error: function(xhr, status, error) {
            console.log('Request failed. ' + error);
        }
    });
    

    // column chart




})(jQuery);