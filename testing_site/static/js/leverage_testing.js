
var tsc_ctx;
var tsc_chart;

var time_min = 0;
var time_max = 99;

var leveragedCloseData=[];

var ol_chart;
var x_values = [];
var y_values = [];



// Function to fetch optimal leverage data and update the chart
function fetchAndUpdateOptimalLeverageChart() {
    // Make an AJAX request to fetch optimal leverage data from Flask app
    $.ajax({
        url: '/calculate_optimal_leverage',
        type: 'GET',
        success: function (data) {
            // Update data with newly fetched values
            x_values = data.x_values;
            y_values = data.y_values;

            // Clear existing chart
            if (ol_chart) {
                ol_chart.update();
            }
        },
        error: function (error) {
            console.error('Error fetching data:', error);
        }
    });
}

// Function to plot the optimal leverage chart
function plotOptimalLeverageChart() {
    // Create a new Chart instance
    var ctx = document.getElementById('optimalLeverageChart').getContext('2d');
    ol_chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: x_values,
            datasets: [{
                label: 'Optimal Leverage',
                data: y_values,
                borderColor: 'blue',
                borderWidth: 1,
                fill: false
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Optimal Leverage'
            },
            scales: {
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'X'
                    }
                }],
                yAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Y'
                    }
                }]
            }
        }
    });
}


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

            var leverageChangeData = response.map(function(item) {
                return item.Leveraged_Pct_Change;
            });

            leveragedReturns = response.map(function(item) {
                return item.Leveraged_Returns;
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

// function to update all the statistics and graph
function updateAll() {
    update_stock_price_graph();
    updateTimeRange();
    updateChartWithTicker();
    updateStatistics();
}


updateTimeRange();

// Get the current slider values

update_stock_price_graph();

// Update the chart with the current ticker
// updateChartWithTicker();

updateStatistics();

//update leverage
function updateLeverage(value) {
    $.ajax({
        type: "POST",
        url: "/update_leverage",
        data: { leverage: value },
        success: function(response) {
            console.log(response);
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
    updateAll();
}

 // Function to update slider display
function updateSlider(time_min, time_max) {
    var range = time_max - time_min;
    var percentMin = ((time_min - $("#timeRangeSlider").slider("option", "time_min")) / range) * 100;
    var percentMax = ((time_max - $("#timeRangeSlider").slider("option", "time_min")) / range) * 100;
    $("#timeRangeSlider").css('background', 'linear-gradient(to right, #007bff ' + percentMin + '%, #007bff ' + percentMax + '%, #ced4da ' + percentMax + '%, #ced4da 100%)');
}

//updates the statistics of the stock
function updateStatistics() {
    $.ajax({
        type: "GET",
        url: "/get_statistics",
        success: function(response) {
            console.log(response);
            //leveraged statistics
            $('#sharpeRatio2').text(response.l_sharpe_ratio);
            $('#cagr2').text(response.l_annual_return);
            $('#volatility2').text(response.l_annual_volatility);
            $('#cumulativeReturn2').text(response.l_cumulative_return);
            //sortino ratio
            $('#sortinoRatio2').text(response.l_sortino_ratio);
            //maximum drawdown
            $('#maxDrawdown2').text(response.l_max_drawdown);

            //stock statistics
            $('#sharpeRatio1').text(response.sharpe_ratio);
            $('#cagr1').text(response.annual_return);
            $('#volatility1').text(response.annual_volatility);
            $('#cumulativeReturn1').text(response.cumulative_return);
            //sortino ratio
            $('#sortinoRatio1').text(response.sortino_ratio);
            //maximum drawdown
            $('#maxDrawdown1').text(response.max_drawdown);
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
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

    // // Add event listener to "Calculate" button
    $('#calculateBtn').click(function() {
        fetchAndUpdateOptimalLeverageChart();
    });

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
        updateAll();
    });

    // Event listener for the leverage range slider
    $('#leverageRange').on('input', function() {
        var value = $(this).val();
        $.ajax({
            type: "POST",
            url: "/update_leverage",
            data: { leverage: value },
            success: function(response) {
                console.log(response);
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
        updateLeverage(value);
        updateLeverageAmount(value);
        updateAll();
    });


    //event listener for start date slider
    $('#start_date').on('input', function() {
        var value = $(this).val();
        updateStartDate(value);
        updateAll();
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
            updateAll();

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