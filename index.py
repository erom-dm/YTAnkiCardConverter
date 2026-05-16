import sys
from pprint import pprint
from youtube_transcript_api import YouTubeTranscriptApi
# from youtube_transcript_api.proxies import GenericProxyConfig
#from youtube_transcript_api.proxies import WebshareProxyConfig

### Generic Proxy API setup
# ytt_api = YouTubeTranscriptApi(
#     proxy_config=GenericProxyConfig(
#         http_url="http://eznihzda:zgs29ujc0qcu@84.247.60.125:6095/",
#         https_url="http://eznihzda:zgs29ujc0qcu@84.247.60.125:6095/",
#     )
# )
### Webshare Proxied API setup
# ytt_api = YouTubeTranscriptApi(
#     proxy_config=WebshareProxyConfig(
#         proxy_username="eznihzda-rotate",
#         proxy_password="zgs29ujc0qcu",
#         domain_name="p.webshare.io",
#         proxy_port=80
#     )
# )
### Regular API setup
ytt_api = YouTubeTranscriptApi()

# user input
# user_input = input("Please provide YT video ID or URL:").split("/watch?v=")
# if (len(user_input) == 1):
#     video_id = user_input[0]
# elif (len(user_input) == 2):
#     video_id = user_input[1]
# else:
#     video_id = None
video_id = "J2y1wVCD9hI"
if (video_id):
    try:
        transcript_list = ytt_api.list(video_id) #languages=['nl', 'en']
        nl_transcript = transcript_list.find_transcript(['nl'])
        original_transcript = nl_transcript.fetch()
        translated_transcript = nl_transcript.translate('en').fetch()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit()
else:
    print("Error: Missing video ID. Exiting script")
    sys.exit()

print(' ===== Original transcript:')
print(f"  Number of snippets: {len(original_transcript)}")
for snippet in original_transcript:
    pprint(snippet.text, indent=2, width=40)

print(' ===== English auto-translated transcript:')
print(f"  Number of snippets: {len(translated_transcript)}")
for snippet in translated_transcript:
    pprint(snippet.text, indent=2, width=40)