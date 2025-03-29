import os, requests
from utils.date_util import convert_utc_to_ist

def get_yt_playlist_data(playlist_id):

    required_keys = ["part", "maxResults", "YT_DATA_API_V3_KEY"]
    for var in required_keys:
        if not os.environ.get(var):
            raise ValueError(f"Missing required environment variable: {var}")

    part = os.environ.get("part")
    max_results = int(os.environ.get("maxResults", 50))  #Default 50
    api_key = os.environ.get("YT_DATA_API_V3_KEY")

    #yt-data-v3 api url - get playlist items
    url = f"https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        "part": part,
        "playlistId": playlist_id,
        "maxResults": max_results,
        "key": api_key
    }
    
    all_videos = []
    while True:
        #GET request to fetch data
        response = requests.get(url, params=params).json()
        # Add fetched items to list
        all_videos.extend(response.get("items", []))

        # Check if there is another page
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

        # Update params to fetch next page
        params["pageToken"] = next_page_token

    return all_videos

def fetch_playlist_metadata(playlist_id):
    
    videos = get_yt_playlist_data(playlist_id)
    count=0
    videos_list = []
    for video in videos:
        count+=1
        snippet = video.get("snippet", {})
        position = snippet.get("position",-1)
        title = snippet.get("title", "Unknown Title")
        resource_id = snippet.get("resourceId",{})
        video_id = resource_id.get("videoId","Unknown Video ID")
        published_at = snippet.get("publishedAt","Unknown Date")
        channel_name = snippet.get("videoOwnerChannelTitle","Unknown Channel")
        channel_id = snippet.get("videoOwnerChannelId","Unknown Channel ID")
            
        thumbnails = snippet.get("thumbnails",{})
        default_thumb = thumbnails.get("default",{})
        thumbnail_url = default_thumb.get("url","No Thumbnail")
        video_dict = {
            'S. No.': position+1,
            'Title': title,
            'Published At': convert_utc_to_ist(published_at), 
            'Channel Name': channel_name,
            'Video URL': f"youtube.com/video/{video_id}",
            'Channel URL': f"youtube.com/channel/{channel_id}",
            'Channel ID': channel_id,
            'Video ID': video_id, 
            'Thumbnail URL': thumbnail_url
        }
        videos_list.append(video_dict)
    
    return videos_list