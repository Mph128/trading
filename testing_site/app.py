from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/leverage_testing')
def leverage_testing():
    

    #return render_template('leverage_testing.html')
    return render_template('leverage_testing.html')


@app.route('/chart')
def chart():
    labels = ['A', 'B', 'C', 'D', 'E']
    data = [random.randint(1, 10) for _ in range(len(labels))]  # Generate random data

    return render_template('chart.html', labels=labels, data=data)

@app.route('/update_time', methods=['POST'])
def update_time():
    min_value = int(request.form['time_min'])
    max_value = int(request.form['time_max'])

    # use min_value and max_value to update the chart
    #.............

    # returns the range to console
    return jsonify({'time_min': min_value, 'time_max': max_value})

@app.route('/update_leverage', methods=['POST'])
def update_leverage():
    value = request.form['leverage']

    # use value to update the chart
    #.............

    # returns the range to console
    return jsonify({'leverage': value})



if __name__ == '__main__':
    app.run(debug=True)
