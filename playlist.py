import os
import google.auth
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Set the path to the credentials file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'Path\to\your\credential\json\file' # <-- edit here

# Get the credentials
creds, project_id = google.auth.default(scopes=['https://www.googleapis.com/auth/youtube.force-ssl'])

# Build the API client
youtube = build('youtube', 'v3', credentials=creds)

# Set the ID of the playlist you want to extract
playlist_id = 'your youtube playlist ID'  # <-- edit here

# Get the first page of the playlist items
request = youtube.playlistItems().list(
    part='snippet',
    playlistId=playlist_id,
    maxResults=50
)
response = request.execute()

# Keep looping until all pages have been processed
while request is not None:
    # Get the next page of playlist items
    next_page_token = response.get('nextPageToken')
    items = response.get('items', [])

    # Extract the video IDs from the playlist items
    video_ids = [item['snippet']['resourceId']['videoId'] for item in items]

    # Save the video IDs to a file
    with open('video_ids.txt', 'a') as f:
        for video_id in video_ids:
            f.write(f'https://youtu.be/{video_id}\n')

    # Exit the loop if there are no more pages
    if next_page_token is None:
        break

    # Prepare the next page request
    request = youtube.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=50,
        pageToken=next_page_token
    )
    response = request.execute()
