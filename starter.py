
# start up the playlist_download.py process


from os import system
import time
import datetime
import youtube_upload_lib


youtube_upload_lib.logger("Starting starter.py","w")

while True:
        
    #start_file = open("control.txt")
    if "start" in open("control.txt","r").read():
        youtube_upload_lib.logger("In starter.py - starting...","a")
        print("STARTING")
        system("python3 playlist_download5.py")
        youtube_upload_lib.logger("In starter.py - kicked out of playlist_download#.py...","a")
        
        
    elif "stop" in open("control.txt","r").read():
        print("STOPPING")
        system("pkill youtube-download")
        youtube_upload_lib.logger("In starter.py - pkill youtube-download...","a")
        
    #open("control.txt","w").write(str(datetime.datetime.now()) + " waiting...")
    #youtube_upload_lib.logger("In starter.py - in while loop...","a")
    
    #print("WAITING")
    #open("/home/jo/Dropbox/youtube_streaming/capture_playlist_location.txt","w").write(str(time.ctime) + " Playlists unchanged... sleeping for 30 seconds.")
    time.sleep(60)
        
