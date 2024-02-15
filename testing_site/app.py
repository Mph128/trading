from flask import Flask, render_template, jsonify, request
import json
from processing import leverage_testing as lt


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

leverage_data = lt.LeverageTesting('SPY','1d')

@app.route('/leverage_testing')
def leverage_testing():

    #return render_template('leverage_testing.html')
    return render_template('leverage_testing.html')


@app.route('/update_time', methods=['POST'])
def update_time():
    min_value = float(request.form['time_min'])
    max_value = float(request.form['time_max'])

    # use min_value and max_value to update the chart
    #.............
    leverage_data.set_time_range_percentage(min_value, max_value)
    # returns the range to console
    return jsonify({'time_min': min_value, 'time_max': max_value})

@app.route('/update_leverage', methods=['POST'])
def update_leverage():
    value = request.form['leverage']

    # use value to update the chart
    #.............

    # returns the range to console
    return jsonify({'leverage': value})


@app.route('/update_ticker', methods=['POST'])
def update_ticker():
    value = request.form['ticker']

    # use value to update the chart
    #.............

    # returns the range to console
    return jsonify({'ticker': value})

@app.route('/get_time_range', methods=['GET'])
def get_time_range():
    data = {
        'start_time': leverage_data.get_start_date(),
        'end_time': leverage_data.get_end_date()
    }
    return jsonify(data)

@app.route('/get_stock_data', methods=['GET'])
def get_stock_data():
    data = leverage_data.close_prices.to_dict(orient='records')
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
