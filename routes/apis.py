from flask import Blueprint, jsonify
from flask_cors import CORS
from utils.constants import status_codes

apis = Blueprint('apis', __name__)
CORS(apis, resources={r"/*": {"origins": "*"}})

#pre-request middleware
@apis.before_request
def before_request():
    pass

@apis.route('/test",methods=["GET"]')
def test_route():
    return jsonify('Success'), status_codes.HTTP_200_OK
