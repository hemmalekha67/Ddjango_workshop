from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import django 

app = Flask(__name__)
CORS(app)

def calculate_bmi(weight, height, unit_system):
    if unit_system == 'metric':
        height_m = height / 100
        bmi = weight / (height_m * height_m)
    else:
        bmi = (weight * 703) / (height * height)

    bmi = round(bmi, 2)

    if bmi < 18.5:
        classification = 'Underweight'
        healthRisk = 'Low'
    elif 18.5 <= bmi < 25:
        classification = 'Normal weight'
        healthRisk = 'Average'
    elif 25 <= bmi < 30:
        classification = 'Overweight'
        healthRisk = 'Mildly increased'
    elif 30 <= bmi < 35:
        classification = 'Obese Class 1'
        healthRisk = 'Moderate'
    elif 35 <= bmi < 40:
        classification = 'Obese Class 2'
        healthRisk = 'Severe'
    else:
        classification = 'Obese Class 3'
        healthRisk = 'Very Severe'

    if unit_system == 'metric':
        normal_weight = 24 * height_m * height_m
    else:
        normal_weight = (24 * height * height) / 703

    weight_diff = round(weight - normal_weight, 2)

    if weight_diff > 10:
        weightAdvice = f'You need to lose {weight_diff} {"kilograms" if unit_system == "metric" else "pounds"}.'
    elif weight_diff > 0:
        weightAdvice = 'Your weight is perfect. Try to maintain it!!!'
    else:
        weightAdvice = f'You need to gain {abs(weight_diff)} {"kilograms" if unit_system == "metric" else "pounds"}.'

    return bmi, classification, healthRisk, weightAdvice

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate_bmi', methods=['POST'])
def calculate_bmi_endpoint():
    data = request.get_json()
    unit_system = data.get('unitSystem')
    weight = data.get('weight')
    height = data.get('height')

    bmi, classification, healthRisk, weightAdvice = calculate_bmi(weight, height, unit_system)

    return jsonify({
        'bmi': bmi,
        'classification': classification,
        'healthRisk': healthRisk,
        'weightAdvice': weightAdvice
    })

if __name__ == '__main__':
    app.run(debug=True)
