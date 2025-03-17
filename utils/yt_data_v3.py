import os, requests

def fetch_playlist_metadata(api_key, playlist_id):
    print('Entering')

    required_vars = ["part", "YT_PLAYLIST_ID", "maxResults", "YT_DATA_API_V3_KEY"]
    for var in required_vars:
        if not os.environ.get(var):
            raise ValueError(f"Missing required environment variable: {var}")

    part = os.environ.get("part")
    playlist_id = os.environ.get("YT_PLAYLIST_ID")
    max_results = int(os.environ.get("maxResults", 50))  #Default 50
    api_key = os.environ.get("YT_DATA_API_V3_KEY")

    url = f"https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        "part": part,
        "playlistId": playlist_id,
        "maxResults": max_results,
        "key": api_key
    }
    
    all_videos = []
    while True:
        response = requests.get(url, params=params).json()
        # Add fetched items to list
        all_videos.extend(response.get("items", []))

        # Check if there is another page
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break  # Exit loop if no more pages

        # Update params to fetch next page
        params["pageToken"] = next_page_token

    return all_videos

# # Example usage
# API_KEY = "YOUR_API_KEY"
# PLAYLIST_ID = "YOUR_PLAYLIST_ID"

# videos = fetch_all_playlist_videos(API_KEY, PLAYLIST_ID)

# # Print results
# for video in videos:
#     title = video["snippet"]["title"]
#     video_id = video["snippet"]["resourceId"]["videoId"]
#     published_at = video["snippet"]["publishedAt"]
#     print(f"Title: {title}, Video ID: {video_id}, Published At: {published_at}")
