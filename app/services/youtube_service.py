from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

API_KEY = os.environ.get('API_KEY')
youtube = build('youtube', 'v3', developerKey=API_KEY)

async def get_channel_id(channel_name):
    try:
        search_response = youtube.search().list(
            q=channel_name,
            part='id',
            type='channel',
            maxResults=20
        ).execute()

        channel_id = search_response.get('items')[0]['id']['channelId']
        return channel_id
    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred: {e.content}')
        return None

async def get_channel_playlists(playlist_ids):
    playlists = []

    try:
        batch = youtube.new_batch_http_request()

        for playlist_id in playlist_ids:
            batch.add(youtube.playlists().list(
                part='snippet',
                id=playlist_id
            ), callback=lambda request_id, response, exception: process_playlist(response, exception, playlists))

        batch.execute()

        return playlists

    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred: {e.content}')
        return []

def process_playlist(response, exception, playlists):
    if exception is not None:
        print(f'An error occurred: {exception}')
        return

    playlist = response.get('items', [])[0]
    playlist_id = playlist['id']
    playlist_title = playlist['snippet']['title']
    playlist_description = playlist['snippet']['description']

    # Retrieve videos within the playlist
    playlist_videos_response = youtube.playlistItems().list(
        part='snippet',
        playlistId=playlist_id,
        maxResults=20  # Adjust the number of videos to retrieve as needed
    ).execute()

    playlist_videos = playlist_videos_response.get('items', [])
    videos = []
    for video in playlist_videos:
        video_id = video['snippet']['resourceId']['videoId']
        video_title = video['snippet']['title']
        videos.append({'video_id': video_id, 'title': video_title})

    playlists.append({
        'playlist_id': playlist_id,
        'title': playlist_title,
        'description': playlist_description,
        'playlist_videos': videos
    })
