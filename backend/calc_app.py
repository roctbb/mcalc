from copy import deepcopy

from flask import Flask, jsonify, request, make_response, abort
from config import *
from validators import get_errors
from helpers import *
from flask_cors import CORS
from flask_migrate import Migrate
from models import *

app = Flask(__name__)

db_string = "postgresql://{}:{}@{}:{}/{}".format(DB_LOGIN, DB_PASSWORD, DB_HOST, DB_PORT, DB_DATABASE)
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/calc', methods=['GET'])
def get_calc_list():
    calcs = Calc.query.all()

    return jsonify([
        {"id": calc.id, "title": calc.title} for calc in calcs
    ])


@app.route('/calc/<int:id>', methods=['GET'])
def get_calc(id):
    calc = Calc.query.filter_by(id=id).first_or_404()
    payload = calc.payload

    if not payload:
        abort(404)

    return jsonify({
        "fields": payload['fields'],
        "title": payload['title'],
        "info": payload['info']
    })


@app.route('/calc/<int:id>', methods=['POST'])
def get_result():
    data = request.json

    calc = Calc.query.filter_by(id=id).first_or_404()
    payload = calc.payload

    if not payload:
        abort(404)

    fields = payload['fields']

    errors = get_errors(data, fields)

    if errors:
        return make_response(jsonify({'state': 'error', 'errors': errors}), 422)

    results = []

    for output in example_calc['results']:
        calculator = import_code(output['script'], 'calculator')

        result = calculator.calculate(deepcopy(data))

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
