Hi!

The code in this repository is part of a project to create an "assembly line" for downloading interesting YouTube content and re-uploading it on my own account. I consciously only use videos that I know are in the public domain, i.e., videos that have been created with public funds (typically in the USA, see https://en.wikipedia.org/wiki/Public_domain#Government_works ).

In order to run this command line program, run the file starter.py . There may be some absolute file paths in parts of the code that would only work on my computer - if you encounter that please adjust them accordingly. Also, the YouTube upload API's client_secrets.json has been removed. When you run this code it will only download videos. You need you own client_secrets.json to make this part of the program work.

What does this program even do???
1. There is (/ was) a program loop running continually on my computer to check if a specific file in my Dropbox is not telling the program to stop.
2. If the program is not supposed to stop, used video playlists specified in _0_playlist_input.txt to download the meta-data of the contained videos. The videos are ranked by viewcount.
3. These videos are then downloaded in order of viewcount one at a time and re-upload with some additional meta-data on my account ( https://www.youtube.com/channel/UCRfEI0VxwKtzcxVzZaQSBkA ).

In total about 4800 videos have been uploaded in this way. I want to clarify that this is a toy project meant to use public domain data without monetization.
