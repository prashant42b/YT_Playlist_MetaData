import io, traceback, requests, os
from flask import Blueprint, jsonify, Response
from flask_cors import CORS
from utils.constants import status_codes
from utils.yt_data_v3 import fetch_playlist_metadata
import pandas as pd

apis = Blueprint('apis', __name__)
CORS(apis, resources={r"/*": {"origins": "*"}})

#pre-request middleware
@apis.before_request
def before_request():
    pass

@apis.route('/test',methods=["GET"])
def test_route():
    return jsonify({'message':'Success'}), status_codes.HTTP_200_OK

@apis.route('/ytdata/download_csv/<string:playlist_id>', methods=["GET"])
def download_csv(playlist_id):
    try:
        if not playlist_id:
            return jsonify({'message': 'Playlist ID is required'}), status_codes.HTTP_400_BAD_REQUEST
        
        #yt-data-v3 api url - playlist name
        required_keys = ["part", "YT_DATA_API_V3_KEY"]
        for var in required_keys:
            if not os.environ.get(var):
                raise ValueError(f"Missing required environment variable: {var}")

        part = os.environ.get("part")
        api_key = os.environ.get("YT_DATA_API_V3_KEY")
        
        url = f"https://www.googleapis.com/youtube/v3/playlists"
        params = {
            "part": part,
            "id": playlist_id,
            "key": api_key
        }
        response = requests.get(url, params=params).json()
        playlist_info = response.get("items", [])[0]
        snippet = playlist_info.get("snippet", {})
        playlist_title = snippet.get("title", "Unknown Title")
        channel_title = snippet.get("channelTitle", "Unknown Channel")
        data = fetch_playlist_metadata(playlist_id)
        
        #Create a Pandas dataframe from the data.
        df = pd.DataFrame(data)
        columns_to_remove = []
        rename_columns = {'Channel Name': 'Channel', 'Published At': 'Published Date'}
        #Remove unwanted columns if any
        if columns_to_remove:
            df = df.drop(columns=columns_to_remove)
        # Rename columns
        if rename_columns:
            df = df.rename(columns=rename_columns)
            
        csv_file = io.StringIO() # Use an in-memory buffer to write the CSV file
        df.to_csv(csv_file, index=False) # Convert the dataframe to an XlsxWriter CSV object.
        csv_file.seek(0)  # Set the file object's position to the beginning
        
        return Response(
        csv_file.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": f'attachment;filename="{playlist_title} - {channel_title}.csv"'}
    )
        
    except Exception as e:
        print(f"Error downloading CSV: {e}")
        traceback.print_exc()
        return jsonify({'message': 'Internal Server Error'}), status_codes.HTTP_500_INTERNAL_SERVER_ERROR
        
