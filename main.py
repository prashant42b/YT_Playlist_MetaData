from flask import Flask, g
from dotenv import load_dotenv
from utils import yt_data_v3
load_dotenv()


app = Flask(__name__)
# app.register_blueprint(homepage,url_prefix='/api/v1/homepage')
# app.register_blueprint(driver_app,url_prefix='/api/v1/driver_app')
# app.register_blueprint(login,url_prefix='/api/v1/login')

# @app.before_request
# def before_request():
#     g.mongo_client = mongo_client

if __name__ == '__main__':
    app.run(debug=True)
    data = yt_data_v3.fetch_playlist_metadata()
    print(data)