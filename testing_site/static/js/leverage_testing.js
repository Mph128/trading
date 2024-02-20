
var tsc_ctx;
var tsc_chart;

var time_min = 0;
var time_max = 99;

var leveragedCloseData=[];


function update_stock_price_graph() {
    $.ajax({
        url: '/get_stock_data',
        type: 'GET',
        success: function(response) {
            // Extract data from the response
            var closeData = response.map(function(item) {
                return item.Close;
            });

            var dateLabels = response.map(function(item) {
                return item.Formatted_Date;
            });

            var changeData = response.map(function(item) {
                return item.Pct_Change;
            });
            

            if (tsc_ctx) {
                // get the range of the time slider and determine the start and end index of the data to be displayed
                console.log('time_min: ', time_min);
                console.log('time_max: ', time_max);
                var startIndex = Math.floor(closeData.length * time_min / 99);
                var endIndex = Math.floor(closeData.length * time_max / 99);

                // Extract the data to be displayed
                var middleCloseData = closeData.slice(startIndex, endIndex);
                var middleDateLabels = dateLabels.slice(startIndex, endIndex);
                var middleChangeData = changeData.slice(startIndex, endIndex);

                //get the start price of the middle data
                var startPrice = middleCloseData[0];
                leveragedCloseData=[];
                //add the start price to the leveragedCloseData array
                leveragedCloseData.push(startPrice);

                // reset the leveragedCloseData array
                leveragedChangeData=[];

                //calculate the leveraged close price
                var leveragedChangeData = middleChangeData.map(function(item) {
                    return (item * $('#leverageRange').val()+1);
                });

                //calculate the leveraged close prices
                for (var i = 0; i < leveragedChangeData.length; i++) {
                    startPrice = startPrice * (leveragedChangeData[i]);
                    leveragedCloseData.push(startPrice);
                }

                console.log('middle daily change: ', middleChangeData)
                console.log('middle close price: ', middleCloseData);
                console.log('leveraged daily change: ', leveragedChangeData);
                console.log('leveraged close price: ', leveragedCloseData);

                // Update the existing chart
                tsc_chart.data.datasets[0].data = middleCloseData;
                tsc_chart.data.labels = middleDateLabels;
                tsc_chart.data.datasets[1].data = leveragedCloseData;
                tsc_chart.update(); // Update the chart
            } else {
                // Create the chart
                leveragedCloseData = closeData;
                tsc_ctx = document.getElementById('timeStockChart').getContext('2d');
                tsc_chart = new Chart(tsc_ctx, {
                    type: 'line',
                    data: {
                        labels: dateLabels,
                        datasets: [{
                            label: 'Stock Price',
                            data: closeData,
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1,
                            fill: false
                        },
                        {
                            label: 'Leveraged Stock Price',
                            data: leveragedCloseData,
                            borderColor: 'rgba(255, 99, 132, 1)',
                            borderWidth: 1,
                            fill: false
                        }]
                    },
                    options: {
                        plugins: {
                            title: {
                                display: true,
                                text: 'SPY',
                                fontSize: 18
                            }
                        },
                        scales: {
                            x: {
                                type: 'category', // Assuming 'Formatted_Date' is categorical data
                                title: {
                                    display: true,
                                    text: 'Date'
                                }
                            },
                            y: {
                                title: {
                                    display: true,
                                    text: 'Close Price'
                                }
                            }
                        }
                    }
                });
            }
        },
        error: function(xhr, status, error) {
            // Handle errors
            console.error(error);
        }
    });
}

 // Function to update the label with the current value of the leverage amount
 function updateLeverageAmount(value) {
     $('#leverageAmount').text(value);
 }

// Function to update the chart with the current ticker
function updateChartWithTicker() {
    // Get the current ticker
    $.ajax({
        url: '/get_ticker',
        type: 'GET',
        success: function(response) {
            // Handle the response data
            console.log(response);
            // Update the chart title with the current ticker
            tsc_chart.options.plugins.title.text = response.ticker;
            // Update the chart
            tsc_chart.update();
        },
        error: function(xhr, status, error) {
            // Handle errors
            console.error(error);
        }
    });
}



 // Function to update the label with the current value of the time range
function updateTimeRange() {
    $.ajax({
        url: '/get_time_range',
        type: 'GET',
        success: function(response) {
            // Handle the response data
            console.log(response);
            // Update the time range label
            $('#timeRangeLabel').text(response.start_time + ' - ' + response.end_time);
        },
        error: function(xhr, status, error) {
            // Handle errors
            console.error(error);
        }
    });
    
}

updateTimeRange();

// Get the current slider values

update_stock_price_graph();

// Update the chart with the current ticker
updateChartWithTicker();

 // Function to update slider display
function updateSlider(time_min, time_max) {
    var range = time_max - time_min;
    var percentMin = ((time_min - $("#timeRangeSlider").slider("option", "time_min")) / range) * 100;
    var percentMax = ((time_max - $("#timeRangeSlider").slider("option", "time_min")) / range) * 100;
    $("#timeRangeSlider").css('background', 'linear-gradient(to right, #007bff ' + percentMin + '%, #007bff ' + percentMax + '%, #ced4da ' + percentMax + '%, #ced4da 100%)');
}


//update start date
function updateStartDate(value) {
    $.ajax({
        type: "POST",
        url: "/update_start_date",
        data: { start_date: value },
        success: function(response) {
            console.log(response);
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}
 
 
 $(function() {

    // Event listener for the ticker submit button
    $('#submitBtn').click(function() {
        $.ajax({
            type: "POST",
            url: "/update_ticker",
            data: {ticker: $('#ticker').val()},
            success: function(response) {
                console.log(response);
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
        updateTimeRange();
        update_stock_price_graph();
        updateChartWithTicker();
    });

    // Event listener for the leverage range slider
    $('#leverageRange').on('input', function() {
        var value = $(this).val();
        updateLeverageAmount(value);
        updateTimeRange();
        update_stock_price_graph();
    });


    //event listener for start date slider
    $('#start_date').on('input', function() {
        var value = $(this).val();
        updateStartDate(value);
        updateTimeRange();
        update_stock_price_graph();
    });



    // Event listener for the time range slider
    $("#timeRangeSlider").slider({
        range: true,
        values: [0, 99],
        slide: function(event, ui) {
            // Update chart based on time range
            // You can implement this logic as needed

            // Get the current slider values
            time_min = ui.values[0];
            time_max = ui.values[1];

            // Update the slider background color
            updateSlider(time_min, time_max);
            // Update the time range label
            updateTimeRange();
            update_stock_price_graph();

            $.ajax({
                type: "POST",
                url: "/update_time",
                data: { time_min: time_min, time_max: time_max },
                success: function(response) {
                    console.log(response);
                },
                error: function(xhr, status, error) {
                    console.error(error);
                }
            });
         }
     });
 });