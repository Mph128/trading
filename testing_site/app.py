from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/leverage_testing')
def leverage_testing():
    return render_template('leverage_testing.html')

@app.route('/chart')
def chart():
    labels = ['A', 'B', 'C', 'D', 'E']
    data = [random.randint(1, 10) for _ in range(len(labels))]  # Generate random data

    return render_template('chart.html', labels=labels, data=data)

@app.route('/update_slider', methods=['POST'])
def update_slider():
    min_value = int(request.form['time_min'])
    max_value = int(request.form['time_max'])

    # Perform any desired operations with the slider values here
    # For example, you can return the values back to the client
    return jsonify({'min': min_value, 'max': max_value})



if __name__ == '__main__':
    app.run(debug=True)
