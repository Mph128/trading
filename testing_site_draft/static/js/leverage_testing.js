var tsc_ctx;
var tsc_chart;
var time_min = 0;
var time_max = 99;
var leveraged_close_data = [];
var ol_chart;
var x_values = [];
var y_values = [];

// Function to fetch optimal leverage data and update the chart
function fetch_and_update_optimal_leverage_chart() {
    // Make an AJAX request to fetch optimal leverage data from Flask app
    $.ajax({
        url: '/calculate_optimal_leverage',
        type: 'GET',
        success: function (data) {
            // Update data with newly fetched values
            x_values = data.ol_x_values;
            // console.log('x_values: ', x_values);
            y_values = data.ol_y_values;
            // console.log('y_values: ', y_values);
            ol_sharpe_ratio_y_values = data.ol_sharpe_ratio_y_values;
            console.log('ol_sharpe_ratio_y_values: ', ol_sharpe_ratio_y_values);

            // Update the chart with the new data
            ol_chart.data.labels = x_values;
            ol_chart.data.datasets[0].data = y_values;
            ol_chart.data.datasets[1].data = ol_sharpe_ratio_y_values;

            ol_chart.update();
        },
        error: function (error) {
            console.error('Error fetching data:', error);
        }
    });
}

// Function to plot the optimal leverage chart
function plot_optimal_leverage_chart() {

    // Make an AJAX request to fetch optimal leverage data from Flask app
    $.ajax({
        url: '/calculate_optimal_leverage',
        type: 'GET',
        success: function (data) {
            // Update data with newly fetched values
            x_values = data.ol_x_values;
            y_values = data.ol_y_values;
            ol_sharpe_ratio_y_values = data.ol_sharpe_ratio_y_values;



            // console.log('x_values: ', x_values);
            // console.log('y_values: ', y_values);

            // Create a new Chart instance
            var ctx = document.getElementById('optimalLeverageChart').getContext('2d');
            ol_chart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: x_values,
                    datasets: [{
                        label: 'Total Return',
                        data: y_values,
                        borderColor: 'blue',
                        borderWidth: 1,
                        fill: false,
                        yAxisID: 'return_y_axis' // Assign this dataset to the primary y-axis
                    },
                    {
                        label: 'Sharpe Ratio',
                        data: ol_sharpe_ratio_y_values,
                        borderColor: 'red',
                        borderWidth: 1,
                        fill: false,
                        yAxisID: 'sharpe_y_axis' // Assign this dataset to the secondary y-axis
                    }]
                },
                options: {
                    labels: {
                        display: true,
                        text: 'Leverage',
                    },
                    title: {
                        display: true,
                        text: 'Optimal Leverage'
                    },
                    scales: {
                        x: {
                            ticks: {
                                precision: 1, // Set the precision to 1 decimal place
                                callback: function(value, index, values) {
                                    return value.toFixed(1)/10; // Format the value as a number with 1 decimal place
                                }
                            },
                            title: {
                                display: true,
                                text: 'Leverage Amount'
                            }
                        },
                        sharpe_y_axis:{
                            type: 'linear',
                            position: 'right',
                            title: {
                                display: true,
                                text: 'Sharpe Ratio'
                            }
                        },
                        return_y_axis:{
                            type: 'linear',
                            position: 'left',
                            title: {
                                display: true,
                                text: 'Return'
                                }
                        }
                    }
                }
            });
        },
        error: function (error) {
            console.error('Error fetching data:', error);
        }
    });
    
    
}

function update_stock_price_graph() {
    $.ajax({
        url: '/get_stock_data',
        type: 'GET',
        success: function(response) {
            // Extract data from the response
            var close_data = response.map(function(item) {
                return item.Close;
            });

            var date_labels = response.map(function(item) {
                return item.Formatted_Date;
            });

            var change_data = response.map(function(item) {
                return item.Pct_Change;
            });

            var leverage_change_data = response.map(function(item) {
                return item.Leveraged_Pct_Change;
            });

            var leveraged_returns = response.map(function(item) {
                return item.Leveraged_Returns;
            });

            if (tsc_ctx) {
                // get the range of the time slider and determine the start and end index of the data to be displayed
                console.log('time_min: ', time_min);
                console.log('time_max: ', time_max);
                var start_index = Math.floor(close_data.length * time_min / 99);
                var end_index = Math.floor(close_data.length * time_max / 99);

                // Extract the data to be displayed
                var middle_close_data = close_data.slice(start_index, end_index);
                var middle_date_labels = date_labels.slice(start_index, end_index);
                var middle_change_data = change_data.slice(start_index, end_index);

                //get the start price of the middle data
                var start_price = middle_close_data[0];
                leveraged_close_data = [];
                //add the start price to the leveraged_close_data array
                leveraged_close_data.push(start_price);

                // reset the leveraged_close_data array
                leverage_change_data = [];

                //calculate the leveraged close price
                leverage_change_data = middle_change_data.map(function(item) {
                    return (item * $('#leverageRange').val()+1);
                });

                //calculate the leveraged close prices
                for (var i = 0; i < leverage_change_data.length; i++) {
                    start_price = start_price * (leverage_change_data[i]);
                    leveraged_close_data.push(start_price);
                }

                console.log('middle daily change: ', middle_change_data)
                console.log('middle close price: ', middle_close_data);
                console.log('leveraged daily change: ', leverage_change_data);
                console.log('leveraged close price: ', leveraged_close_data);

                // Update the existing chart
                tsc_chart.data.datasets[0].data = middle_close_data;
                tsc_chart.data.labels = middle_date_labels;
                tsc_chart.data.datasets[1].data = leveraged_close_data;
                tsc_chart.update(); // Update the chart
            } else {
                // Create the chart
                leveraged_close_data = close_data;
                tsc_ctx = document.getElementById('timeStockChart').getContext('2d');
                tsc_chart = new Chart(tsc_ctx, {
                    type: 'line',
                    data: {
                        labels: date_labels,
                        datasets: [{
                            label: 'Stock Price',
                            data: close_data,
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1,
                            fill: false
                        },
                        {
                            label: 'Leveraged Stock Price',
                            data: leveraged_close_data,
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
function update_leverage_amount(value) {
     $('#leverageAmount').text(value);
}

// Function to format value as percentage with 3 decimal places
function formatPercentage(value) {
    return (value * 100).toFixed(3) + '%';
}

// Function to update the chart with the current ticker
function update_chart_with_ticker() {
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
function update_time_range() {
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

// Function to update all the statistics and graph
function update_all() {
    update_stock_price_graph();
    update_chart_with_ticker();
    update_statistics();
    fetch_and_update_optimal_leverage_chart();
    update_time_range();
}

update_time_range();
update_stock_price_graph();
update_statistics();
plot_optimal_leverage_chart();

//update leverage
function update_leverage(value) {
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
    update_all();
}

// Function to update slider display
function update_slider(time_min, time_max) {
    var range = time_max - time_min;
    var percent_min = ((time_min - $("#timeRangeSlider").slider("option", "time_min")) / range) * 100;
    var percent_max = ((time_max - $("#timeRangeSlider").slider("option", "time_min")) / range) * 100;
    $("#timeRangeSlider").css('background', 'linear-gradient(to right, #007bff ' + percent_min + '%, #007bff ' + percent_max + '%, #ced4da ' + percent_max + '%, #ced4da 100%)');
}

//updates the statistics of the stock
function update_statistics() {
    $.ajax({
        type: "GET",
        url: "/get_statistics",
        success: function(response) {
            console.log(response);
            // Update the card text with formatted values
            //unleveraged statistics
            $('#sharpeRatio1').text(formatPercentage(response.sharpe_ratio));
            $('#sortinoRatio1').text(formatPercentage(response.sortino_ratio));
            $('#maxDrawdown1').text(formatPercentage(response.max_drawdown));
            $('#cagr1').text(formatPercentage(response.annual_return));
            $('#volatility1').text(formatPercentage(response.annual_volatility));
            $('#cumulativeReturn1').text(formatPercentage(response.cumulative_return));

            //leveraged statistics
            $('#sharpeRatio2').text(formatPercentage(response.l_sharpe_ratio));
            $('#sortinoRatio2').text(formatPercentage(response.l_sortino_ratio));
            $('#maxDrawdown2').text(formatPercentage(response.l_max_drawdown));
            $('#cagr2').text(formatPercentage(response.l_annual_return));
            $('#volatility2').text(formatPercentage(response.l_annual_volatility));
            $('#cumulativeReturn2').text(formatPercentage(response.l_cumulative_return));
        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
}

//update start date
function update_start_date(value) {
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
        update_all();
    });

    // Event listener for the leverage range slider to change the leverage amount shown
    $('#leverageRange').on('input', function() {
        var value = $(this).val();
        update_leverage_amount(value);
    });

     // Event listener for the leverage range slider to update the leverage data
     $('#leverageRange').on('change', function() {
        var value = $(this).val();
        update_leverage(value);
        update_all();
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
            update_slider(time_min, time_max);
            
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

            // Update the time range label
            update_time_range();
        },
        change: function(event, ui) {
        // Update chart based on time range
        // You can implement this logic as needed

        // Get the current slider values
        time_min = ui.values[0];
        time_max = ui.values[1];

        // Update the slider background color
        update_slider(time_min, time_max);


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

        update_all();
        } 
    });
 });
