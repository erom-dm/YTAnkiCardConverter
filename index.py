import sys
from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()

user_input = input().split("/watch?v=")
if (len(user_input) == 1):
    video_id = user_input[0]
elif (len(user_input) == 2):
    video_id = user_input[1]
else:
    video_id = None

if (video_id):
    try:
        transcript = ytt_api.fetch(video_id)
    except Exception:
        print("Error: Provided video ID was invalid. Exiting script")
        sys.exit()
else:
    print("Error: Missing video ID. Exiting script")
    sys.exit()
print(transcript)