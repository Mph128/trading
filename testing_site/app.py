from flask import Flask, render_template, jsonify, request
import json
from processing import leverage_testing as lt
import markdown


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

leverage_data = lt.LeverageTesting('spy', '1d')

@app.route('/leverage_testing')
def leverage_testing():
    with open('docs\leverage_testing.md', 'r') as f:
        markdown_content = f.read()

    # Convert Markdown to HTML
    html_content = markdown.markdown(markdown_content)

    #return render_template('leverage_testing.html')
    return render_template('leverage_testing.html',markdown_content=html_content)


# calculates optimal leverage
@app.route('/calculate_optimal_leverage', methods=['POST'])
def calculate_optimal_leverage():
    # calculate the optimal leverage equation
    x_values, y_values, peaks = leverage_data.calculate_leverage_equation()

    # returns the optimal leverage to console
    return jsonify({'x_values': x_values, 'y_values': y_values, 'peaks': peaks})


#route to get the statistics
@app.route('/get_leveraged_statistics', methods=['GET'])
def get_statistics():

    #get the risk free rate from the form

    

    data = {
        'l_sharpe_ratio': leverage_data.get_leveraged_sharpe_ratio(),
        'l_sortino_ratio': leverage_data.get_sortino_ratio(),
        'l_max_drawdown': leverage_data.get_max_drawdown(),
        'l_annual_return': leverage_data.get_annual_return(),
        'l_annual_volatility': leverage_data.get_annual_volatility(),
        'l_cumulative_return': leverage_data.get_cumulative_return()

    }
    return jsonify(data)


# route to update the start date
@app.route('/update_start_date', methods=['POST'])
def update_start_date():
    value = request.form['start_date']

    # use value to update the chart
    #.............
    leverage_data.set_start_date(value)

    # returns the range to console
    return jsonify({'start_date': value})


@app.route('/update_time', methods=['POST'])
def update_time():
    min_value = float(request.form['time_min'])
    max_value = float(request.form['time_max'])

    # use min_value and max_value to update the chart
    #.............
    leverage_data.set_time_range_percentage(min_value, max_value)

    # returns the range to console
    return jsonify({'time_min': min_value, 'time_max': max_value})


@app.route('/update_ticker', methods=['POST'])
def update_ticker():
    value = request.form['ticker']

    # use value to update the chart
    try:
        leverage_data.update_data_from_ticker(value)
    except:
        return jsonify({'ticker': 'Invalid Ticker'})

    # returns the range to console
    return jsonify({'ticker': value})

# route to get the current ticker
@app.route('/get_ticker', methods=['GET'])
def get_ticker():
    data = {
        'ticker': leverage_data.get_ticker()
    }
    print(data)
    return jsonify(data)


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
