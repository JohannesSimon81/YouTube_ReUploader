





import pafy
import time
import os
import subprocess
from timeit import default_timer as timer
import datetime


def logger(msg, write_mode):
    open("/home/jo/Dropbox/youtube_streaming/log.txt",write_mode).write(msg + " - " + str(datetime.datetime.now()) + "\n" )
        
        
def exec_cmd(cmd, timeout=1800):
    timer = 0
    num_upload_tries = 0
    num_upload_tries_max = 2
    p = subprocess.Popen(cmd,shell=True)
    while(timer < timeout):
        time.sleep(1)
        timer += 1
        if p.poll() is None:
            if timer == timeout:
                p.kill()
                print("TIMED OUT after " + str(timer) + " sec., KILLED!")
                if num_upload_tries < num_upload_tries_max:
                    num_upload_tries += 1
                    timer = 0
                    p = subprocess.Popen(cmd,shell=True)
        else:
            print(p.communicate())
            print("Finished withing " + str(timer) + " sec.")
            break


def rank_videos(info):
    # Rank the videos by view numbers, likes, video age, etc.
    likes_num = int(info["likes"])
    dislikes_num = int(info["dislikes"])
    views_num = int(info["views"].replace(".",""))
    video_age = time.time() - int(info["time_created"])
    rank = (likes_num - dislikes_num) * views_num * 1.0 / video_age
    return rank


def get_video_list_info(plurl, keep_ordering):
    # Download all relevant video meta-data, rank videos, and return a
    # list of these data
    video_list = []
    
    playlist = pafy.get_playlist(plurl)

    playlist_description = playlist['title'] + "\n" + playlist['author'] + "\n" + plurl + "\n\n"
    open("_playlists.txt","a").write(playlist_description)

    for i in range(len(playlist['items'])):
        info = playlist['items'][i]['playlist_meta']
        pafy_info = playlist['items'][i]['pafy']
        
        my_rank = rank_videos(info)
        
        #print(info["title"] + "\n" + info["keywords"] + "\n" + str(info["likes"]) + "\n" + str(info["views"]) + "\n" + info["added"] + "\n" + info["duration"] + "\n" + str(info["author"]) + "\n" + str(my_rank) + "\n\n")
           
        video_list.append([my_rank, info, pafy_info])

    if keep_ordering == 2:  
        # sort video_list
        key_index = 0
        video_list = sorted(video_list, key=lambda x: x[key_index], reverse=True)
    elif keep_ordering == 1:
        # reverse video_list
        vid_helper = []
        for i in range(len(video_list)):
            vid_helper.append(video_list[-i-1])
        video_list = vid_helper
    
    return video_list


def create_video_title(title, title_prefix, title_suffix, title_remove):
    title_out = title_prefix + " " + title.replace(title_remove,"") + " " + title_suffix
    if len(title_out) > 100:
        title_out = title_prefix + " " + title.replace(title_remove," ")
        if len(title_out) > 100:
            title_out = title
    title_out = title_out.replace("  "," ")
    return title_out


def create_video_description(video_info, description_addition):
    # Create a description based on the original, a custom addition, and our standard suffix
    # Ensure that the overall length stays beneath 5000 characters
    
    keep_original_description = True
    if " *NOT_ORIGINAL*" in description_addition:
        keep_original_description = False
        description_addition = description_addition.replace(" *NOT_ORIGINAL*","")
    
    description_text = str(description_addition) + "\n\n"
    if keep_original_description:
        description_text += str(video_info["description"]) + "\n\n"
    description_text += open("description_suffix.txt","r").read().replace("_PLACEHOLDER_AUTHOR",video_info["author"]).replace("_PLACEHOLDER_DATE_ADDED",video_info["added"]).replace("_PLACEHOLDER_KEYWORDS",video_info["keywords"])
    #description_text += open("description_suffix.txt","r").read()
    #description_text = description_text.replace('"',' ').replace("'"," ")
    description_text = str(description_text) #

    if len(description_text) > 4995:
        description_text = description_text[:4990] + "..."
    return description_text
    
    
def create_video_upload_string(vid_title, vid_category, vid_keywords, vid_playlist, vid_description, vid_file_location):
    upload_string = ""
    upload_string += 'youtube-upload'
    upload_string += ' --title="' + str(vid_title.replace(u"\u2018", "'").replace(u"\u2019", "'").replace('"',"'")) + '"'
    upload_string += ' --category="' + str(vid_category.replace(u"\u2018", "'").replace(u"\u2019", "'").replace('"',"'")) + '"'
    upload_string += ' --tags="' + str(vid_keywords.replace(u"\u2018", "'").replace(u"\u2019", "'").replace('"',"'")) + '"'
    upload_string += ' --playlist="' + str(vid_playlist.replace(u"\u2018", "'").replace(u"\u2019", "'").replace('"',"'")) + '"'
    upload_string += ' --description="' + str(vid_description.replace(u"\u2018", "'").replace(u"\u2019", "'").replace('"',"'")) + '"'
    upload_string += ' --client-secrets=client_secrets.json '
    #upload_string += ' --file="'+str(vid_file_location.replace(u"\u2018", "'").replace(u"\u2019", "'").replace('"',"'")) + '"'
    upload_string += str(vid_file_location.replace(u"\u2018", "'").replace(u"\u2019", "'").replace('"',"'"))

    open("_upload_string.txt","w").write(upload_string)
    return upload_string
    

    
def download_single_video(video_pafy_info):
    # download and store as video.mp4 (file ending may vary)
    print("Start download @ " + str(time.ctime()))
    logger("\n1","a")
    start = timer()
    
    best = video_pafy_info.getbest()
    print(best)
    logger("\n2","a")
    filename = best.download(filepath="/home/jo/workspace/youtube_streaming/video_folder/")
    logger("\n3","a")
    filename_ending = filename.split(".")[-1]
    logger("\n4","a")
    new_filename = "/home/jo/workspace/youtube_streaming/video_folder/video." + filename_ending
    os.rename(filename, new_filename)
    filename = new_filename
    logger("\n5","a")
    
    end = timer()
    download_duration = end - start
    print("\n" + str(download_duration) + " <--- download duration in seconds")
    #print("Filename = " + filename)
    return filename, download_duration
    
    
def upload_single_video(upload_string):
    tryUpload = True
    tryCount = 0
    while tryUpload:
        print("Start upload @ " + str(time.ctime()))
        start = timer()
        
        #os.system(upload_string + " 2>&1 | tee /home/jo/Dropbox/youtube_streaming/capture_playlist_location.txt")
        exec_cmd(upload_string + " 2>&1 | tee /home/jo/Dropbox/youtube_streaming/capture_playlist_location.txt",3600)
        #os.system(upload_string.replace("youtube-upload","python2 youtube_API_uploader.py") + " 2>&1 | tee /home/jo/Dropbox/youtube_streaming/capture_playlist_location.txt")
        
        end = timer()
        upload_duration = end - start
        print(str(upload_duration) + " <--- upload duration in seconds")
        
        time.sleep(3)
        tryCount += 1
        fin = open("/home/jo/Dropbox/youtube_streaming/capture_playlist_location.txt","r").read()
        if "Connection timed out" in fin:
            tryUpload = True
            if tryCount > 3:
                tryUpload = False
        else:
            tryUpload = False
        
    return upload_duration
    
def get_playlist_upload_location():
    with open("/home/jo/Dropbox/youtube_streaming/capture_playlist_location.txt","r") as f:
        for line in f:
            if "Adding video to playlist:" in line:
                up_loc = line.replace("Adding video to playlist:","").replace(" ","")
                return "https://www.youtube.com/playlist?list="+up_loc
                
def check_upload_quota_limit_OK():
    with open("/home/jo/Dropbox/youtube_streaming/capture_playlist_location.txt","r") as f:
        for line in f:
            if "The user has exceeded the number of videos they may upload." in line:
                return False
    return True
    


def playlist_input():
    pl_list = []
    with open("/home/jo/Dropbox/youtube_streaming/0_playlist_input.txt","r") as f:
        for line in f:
            #print line
            if "#" not in line:
                #print line.split('"')
                if 'plurl' in line:
                    pl = {"plurl": "","vid_playlist": "","title_prefix": "","title_suffix": "","title_remove": "","tags_addition": "","description_addition": "","keep_ordering": 0,"sleep_duration_minutes": 0}
                    pl["plurl"] = line.split('"')[3]
                elif 'vid_playlist' in line:
                    pl["vid_playlist"] = line.split('"')[3]
                elif 'title_prefix' in line:
                    pl["title_prefix"] = line.split('"')[3]
                elif 'title_suffix' in line:
                    pl["title_suffix"] = line.split('"')[3]
                elif 'title_remove' in line:
                    pl["title_remove"] = line.split('"')[3]
                elif 'tags_addition' in line:
                    pl["tags_addition"] = line.split('"')[3]
                elif 'description_addition' in line:
                    pl["description_addition"] = line.split('"')[3]
                elif 'keep_ordering' in line:
                    #if line.split('"')[3] == "True":
                    #   pl["keep_ordering"] = True
                    #else:
                    #   pl["keep_ordering"] = False
                    pl["keep_ordering"] = int(line.split('"')[3])
                elif 'sleep_duration_minutes' in line:
                    pl["sleep_duration_minutes"] = int(line.split('"')[3])
                    pl_list.append(pl)
                    print("Added playlist " + str(len(pl_list)))
    return pl_list


    
def process_all_playlist_videos(playlists, total_video_count_since_quota_reset):
    
    
    total_video_count_all_playlists = 0
    print("..1")
    
    videos_from_this_playlist_counter = 0
    videos_from_this_playlist_counter_max = 1
    number_of_videos_processed_from_any_playlist = 0
    #number_of_videos_processed_from_any_playlist_max = 2
    for playlist_input in playlists:
        
        plurl = playlist_input["plurl"]
        vid_playlist = playlist_input["vid_playlist"]
        title_prefix = playlist_input["title_prefix"]
        title_suffix = playlist_input["title_suffix"]
        title_remove = playlist_input["title_remove"]
        tags_addition = playlist_input["tags_addition"]
        description_addition = playlist_input["description_addition"]
        keep_ordering = playlist_input["keep_ordering"]
        sleep_duration_minutes = playlist_input["sleep_duration_minutes"]
        print("..2")
        
        video_list = get_video_list_info(plurl, keep_ordering)
        #print("len(video_list) = ", len(video_list))
        
        playlist_upload_location = ""
        
        videos_from_this_playlist_counter = 0
        for counter, each in enumerate(video_list):
            if videos_from_this_playlist_counter >= videos_from_this_playlist_counter_max:
                break
            print("..3")
            video_rank = each[0]
            video_info = each[1]
            video_pafy_info = each[2]
            
            #print(video_info["title"])
            
            if not video_info["title"] in open("_titles.txt","r").read() and not str(video_info["title"].encode('ascii', 'ignore').decode('ascii')) in open("_titles.txt","r").read():
                print("..4")

                logger(str(video_info["title"]) + " not yet processed","a")
                # check time for router reset
                # sleep at 2:00 AM for 5 minutes
                now = datetime.datetime.now()
                if now.hour == 2:
                    time.sleep(5*60)

                
                
                
                try:
                    print( (str(video_rank) + "\n" + str(video_info["title"]) + "\n" + str(video_info["author"]) + "\n" + str(video_info["duration"]) + "\n" + str(video_info["views"]) + "\n" + str(video_info["likes"]) + "\n" + str(video_info["dislikes"]) + "\n" + str(video_info["keywords"]) + "\n" + str(video_info["added"])) )
                except:
                    print( "print problem" )
                    pass
                    
                #try:
                if not playlist_upload_location == "":
                    if not playlist_upload_location in description_addition:
                        description_addition = "Find this video's playlist at "+playlist_upload_location+" "+description_addition
                #except:
                #   playlist_upload_location == ""
                #   pass

                logger(str(video_info["title"]) + " just before","a")
                #try:
                vid_file_location, download_duration = download_single_video(video_pafy_info)
                logger(str(video_info["title"]) + " downloaded","a")
                vid_title = create_video_title(str(video_info["title"]), title_prefix, title_suffix, title_remove)
                vid_description = create_video_description(video_info, description_addition)
                vid_keywords = video_info["keywords"].replace('"',"'") + ", " + tags_addition
                vid_category = "Education"
                                    
                                    

                upload_string = create_video_upload_string(vid_title, vid_category, vid_keywords, vid_playlist, vid_description, vid_file_location)
                print(upload_string)
                upload_duration =upload_single_video(upload_string)
                logger(str(video_info["title"]) + " uploaded","a")
                
                videos_from_this_playlist_counter += 1
                number_of_videos_processed_from_any_playlist += 1

                #except:
                #   logger("\nerror in down-/upload process...", "a")
                #   pass
                print("..5")
                            
                while check_upload_quota_limit_OK() == False:
                    print(time.ctime())
                    print("Waiting for 2 hours due to upload quota error.")
                    logger("sleeping due to quota","a")
                    total_video_count_since_quota_reset = 0

                    time.sleep(2*60*60)
                    upload_duration =upload_single_video(upload_string) 
                print("..6")
                total_video_count_since_quota_reset += 1
                open("_quota_count.txt","a").write(str(total_video_count_since_quota_reset) + " === " + str(datetime.datetime.now()) + "\n")
                
                
                playlist_upload_location = get_playlist_upload_location()
                logger("moving on to next video(..?)","a")
                
                
                fin = open("/home/jo/Dropbox/youtube_streaming/capture_playlist_location.txt","r").read()
                if not "Connection timed out" in fin:
                    open("_titles.txt","a").write(str(video_info["title"]) + "\n")
                
                print("\nVideos processed: " + str(counter+1) + "/" + str(len(video_list)) + " @ " + str(time.ctime()))
                total_video_count_all_playlists += 1
                print("--- processed videos from all playlists: " + str(total_video_count_all_playlists))
                print("==============================================================\n")
                    

                print("Taking a nap "+str(sleep_duration_minutes)+" minutes @ " + str(time.ctime()))
                time.sleep(sleep_duration_minutes*60)
                logger(str(video_info["title"]) + " done", "a")

            #else:
            #   print(video_info["title"] + " --- has already been downloaded!\n\n")
    
    print("number_of_videos_processed_from_any_playlist = ", number_of_videos_processed_from_any_playlist)
    return number_of_videos_processed_from_any_playlist
