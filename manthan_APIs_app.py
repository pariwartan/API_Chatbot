from flask import Flask, jsonify
from manthan_data_store import implementation_initiate_response_data, implementation_bind_response_data, implementation_validate_status_response_data

app = Flask(__name__)


@app.route('/manthan/v1/implementation.initiate', methods=['GET'])
def implementation_initiate():
    """
    Initiate an implementation request to onboard a new customer.

    Returns:
        complete API response as JSON and the HTTP status code.
    """
    return jsonify(implementation_initiate_response_data), 200

@app.route('/manthan/v1/implementation.bind', methods=['GET'])
def implementation_bind():
    """
    Bind the implementation object to the ADP domain (payroll, benefits time etc) for onboarding.

    Returns:
        complete API response as JSON and the HTTP status code.
    """
    return jsonify(implementation_bind_response_data), 200

@app.route('/manthan/v1/validations/<validationrefid>/status', methods=['GET'])
def implementation_status_validate(validationrefid):
    """
    Get the validation request status from the earlier performed validation.

    Returns:
        complete API response as JSON and the HTTP status code.
    """
    return jsonify(implementation_validate_status_response_data), 200    


if __name__ == '__main__':
    app.run(debug=True)
