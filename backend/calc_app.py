from flask import Flask, jsonify, request, make_response
from config import *
from validators import get_errors
from helpers import *
from example import example_calc
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/calc', methods=['GET'])
def get_calc():
    return jsonify({
        "fields": example_calc['fields'],
        "title": example_calc['title'],
        "info": example_calc['info']
    })


@app.route('/calc', methods=['POST'])
def get_result():
    data = request.json
    fields = example_calc['fields']

    errors = get_errors(data, fields)

    if errors:
        return make_response(jsonify({'state': 'error', 'errors': errors}), 422)

    results = []

    for output in example_calc['results']:
        calculator = import_code(output['script'], 'calculator')

        print(data)

        result = calculator.calculate(data)

        if "unit" in output:
            if output['unit'] == '%':
                result *= 100

        if "round" in output:
            result = round(result, output['round'])

        results.append({
            "unit": output.get('unit', 'float'),
            "value": result,
            "code": output['code'],
            "title": output['title']
        })

    return jsonify({'state': 'success', 'results': results})

if __name__ == "__main__":
    app.run(HOST, PORT, debug=DEBUG)
