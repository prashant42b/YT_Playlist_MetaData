from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, g, jsonify
from flask_cors import CORS
from utils.yt_data_v3 import fetch_playlist_metadata
from utils.constants import status_codes
from routes.apis import apis


#fetching playlist_metadata if env true
if os.environ.get("DATA_PRELOAD").lower() == "true":
    videos_data = fetch_playlist_metadata()
    print(videos_data)
    
app = Flask(__name__)

# Apply CORS
cors = CORS(app, resources={r"/*": {"origins": "*"}})

#Register route handler blueprint
app.register_blueprint(apis,url_prefix='/api/v1')

#Health check
@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({'message': 'ok'}), status_codes.HTTP_200_OK

#pre-request middleware
@app.before_request
def before_request():
    pass

if __name__ == '__main__':
    app.run(debug=True)