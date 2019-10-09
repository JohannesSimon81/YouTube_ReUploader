
import youtube_upload_lib
import time
import importlib
from datetime import datetime
    

"""
# TEMPLATE
playlist_input = {\
"plurl": "https://www.youtube.com/watch?v=j9WZyLZCBzs&list=PLUl4u3cNGP61MdtwGTqZA0MreSaDybji8",\
"vid_playlist": "Statistics - MIT 6.041 Probabilistic Systems Analysis and Applied Probability, Fall 2010",\
"title_prefix": "Statistics - ",\
"title_suffix": "",\
"title_remove": "",\
"tags_addition": "",\
"description_addition": "More info: "+\
"http://www.esa.int/Our_Activities/Space_Science/Rosetta"\
+"\n"+\
"https://en.wikipedia.org/wiki/Rosetta_(spacecraft)",\
"keep_ordering": True,\
"sleep_duration_minutes": 0\
}
playlists.append(playlist_input)
"""

youtube_upload_lib.logger("Starting playlist_download#.py","a")

while True:

    youtube_upload_lib.logger("In playlist_download#.py: starting out loop","a")
    importlib.reload(youtube_upload_lib)
    playlists = youtube_upload_lib.playlist_input()
    
    print("...")
    
    number_of_videos_processed_from_any_playlist = 1000
    total_video_count_since_quota_reset = 0
    while(number_of_videos_processed_from_any_playlist > 0):
        number_of_videos_processed_from_any_playlist = youtube_upload_lib.process_all_playlist_videos(playlists, total_video_count_since_quota_reset)
    
    youtube_upload_lib.logger("In playlist_download#.py: past playlist_input, playlist_videos","a")
    
    playlists_old = playlists
    
    
    while playlists == playlists_old:
        print("Playlists unchanged... sleeping for 30 seconds.")
        time.sleep(30)
        open("/home/jo/Dropbox/youtube_streaming/capture_playlist_location.txt","w").write(str(time.ctime) + " Playlists unchanged... sleeping for 30 seconds.")
        playlists = youtube_upload_lib.playlist_input()

    youtube_upload_lib.logger("In playlist_download#.py: checked playlists vs old playlist - not identical continue program","a")

