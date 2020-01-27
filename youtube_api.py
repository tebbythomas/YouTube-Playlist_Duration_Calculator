'''
Description:
Program uses YouTube Data API V3 to calculate the total duration
of a YouTube playlist given the URL of the playlist
'''

from apiclient.discovery import build
import json
import os

# YouTube Data API V3 Key
YT_API_KEY = os.environ['YOUTUBE_DATA_API_V3']

# Function to get the video IDs of each video of the playlist
def get_vid_ids_from_playlist(playlist_id, youtube_obj):
    vid_ids = list()
    next_page_token = ""
    # Accessing each of the videos of the plylist - 1 page at a time
    # Each page contains the details of 50 videos
    while next_page_token is not "NA":
        request = youtube_obj.playlistItems().list(
            part="contentDetails",
            maxResults="50",
            pageToken=next_page_token,
            playlistId=playlist_id
        )
        response = request.execute()
        vid_items = response["items"]
        for vid_item in vid_items:
            vid_ids.append(vid_item["contentDetails"]["videoId"])
        if "nextPageToken" in response:
            next_page_token = response["nextPageToken"]
        else:
            next_page_token = "NA"
            break
    return vid_ids

# Function to get the duration of each video
def get_vid_details(vid_ids, youtube_obj):
    vid_details = dict()
    for vid_id in vid_ids:
        request = youtube_obj.videos().list(
        part="snippet,contentDetails",
        id=vid_id
        )
        response = request.execute()
        title = response["items"][0]["snippet"]["title"]
        duration = response["items"][0]["contentDetails"]["duration"][2:]
        vid_details[title] = duration
    return vid_details


if __name__ == "__main__":
    print("Enter the URL of the playlist:")
    playlist_id = input().split("playlist?list=")[1]
    print(f"\nPlaylist ID Extracted: {playlist_id}")
    youtube_obj = build("youtube", "v3", developerKey=YT_API_KEY)
    # Get all the video IDs which are part of the playlist
    vid_ids = get_vid_ids_from_playlist(playlist_id, youtube_obj)
    vid_details = get_vid_details(vid_ids, youtube_obj)
    # Get the duration of each of the videos given the video ID
    hours = 0
    mins = 0
    seconds = 0
    total_duration = 0
    count = 1
    #print("\n\nVideos in playlist:")
    #print(f"\nPlaylist has {len(vid_details)} videos listed below:\n")
    for title, duration in vid_details.items():
        #print(f"{count}. Title: {title}\nDuration: {duration}\n")
        count += 1
        if "H" in duration:
            hours = int(duration.split("H")[0])
            total_duration += 3600 * hours
            duration = duration.split("H")[1]
        if "M" in duration:
            mins = int(duration.split("M")[0])
            total_duration += 60 * mins
            duration = duration.split("M")[1]
        if "S" in duration:
            seconds = int(duration.split("S")[0])
            total_duration += seconds
    #print(f"Duration in seconds: {total_duration}\n")
    total_duration_hrs = int(total_duration/3600)
    total_duration = total_duration % 3600
    total_duration_mins = int(total_duration/60)
    total_duration = total_duration % 60
    total_duration_seconds = int(total_duration)
    print(f"\nPlaylist has {len(vid_details)} videos\n")
    print(f"Total Duration of playlist: {total_duration_hrs} Hours, {total_duration_mins} Minutes, {total_duration_seconds} Seconds\n")
    