// // Generate random data for the first graph (Leverage vs Annualized Returns)
// var leverageData = [];
// var returnsData = [];
// for (var i = 0; i < 10; i++) {
//     leverageData.push(Math.random() * 10); // Random leverage values
//     returnsData.push(Math.random() * 100); // Random annualized returns values
// }

// // Generate random data for the second graph (Time vs Stock Performance)
// var timeData = [];
// var stockData = [];
// for (var i = 0; i < 10; i++) {
//     timeData.push(i); // Time values (0 to 9)
//     stockData.push(Math.random() * 1000); // Random stock performance values
// }

// Create the first chart (Leverage vs Annualized Returns)
// var leverageReturnsChartCtx = document.getElementById('leverageReturnsChart').getContext('2d');
// var leverageReturnsChart = new Chart(leverageReturnsChartCtx, {
//     type: 'scatter',
//     data: {
//         datasets: [{
//             label: 'Leverage vs Annualized Returns',
//             data: leverageData.map((value, index) => ({ x: value, y: returnsData[index] })),
//             backgroundColor: 'rgba(255, 99, 132, 0.5)',
//             borderColor: 'rgba(255, 99, 132, 1)',
//             borderWidth: 1
//         }]
//     },
//     options: {
//         scales: {
//             x: {
//                 type: 'linear',
//                 position: 'bottom'
//             },
//             y: {
//                 type: 'linear',
//                 position: 'left'
//             }
//         }
//     }
// });


//var timeStockChart; // Declare a variable to store the chart instance

function update_stock_price_graph(){

    // if (timeStockChart) {
    //     timeStockChart.labels = ['hello', 'hi'] 
    // }
    // else {
        // Fetch stock data
        // if (timeStockChart) {
        //     // If it exists, destroy it
        //     timeStockChart.destroy();
        // }
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

                // Create the chart
                var tsc_ctx = document.getElementById('timeStockChart').getContext('2d');
                var myChart = new Chart(tsc_ctx, {
                    type: 'line',
                    data: {
                        labels: dateLabels,
                        datasets: [{
                            label: 'Stock Price',
                            data: closeData,
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1,
                            fill: false
                        }]
                    },
                    options: {
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
            },
            error: function(xhr, status, error) {
                // Handle errors
                console.error(error);
            }
        });
    // }
}



 // Function to update the label with the current value of the leverage amount
 function updateLeverageAmount(value) {
     $('#leverageAmount').text(value);
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
    update_stock_price_graph()
}

updateTimeRange();

 // Function to update slider display
 function updateSlider(time_min, time_max) {
     var range = time_max - time_min;
     var percentMin = ((time_min - $("#timeRangeSlider").slider("option", "time_min")) / range) * 100;
     var percentMax = ((time_max - $("#timeRangeSlider").slider("option", "time_min")) / range) * 100;
     $("#timeRangeSlider").css('background', 'linear-gradient(to right, #007bff ' + percentMin + '%, #007bff ' + percentMax + '%, #ced4da ' + percentMax + '%, #ced4da 100%)');
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
    });

     // Event listener for the leverage range slider
     $('#leverageRange').on('input', function() {
         var value = $(this).val();
         updateLeverageAmount(value);

         $.ajax({
             type: "POST",
             url: "/update_leverage",
             data: {leverage: value},
             success: function(response) {
                 console.log(response);
             },
             error: function(xhr, status, error) {
                 console.error(error);
             }
         });
         
     });

     // Event listener for the time range slider
     $("#timeRangeSlider").slider({
         range: true,
         values: [0, 100],
         slide: function(event, ui) {
             // Update chart based on time range
             // You can implement this logic as needed

             // Get the current slider values
             var time_min = ui.values[0];
             var time_max = ui.values[1];

             // Update the slider background color
             updateSlider(time_min, time_max);
             // Update the time range label
             updateTimeRange();

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