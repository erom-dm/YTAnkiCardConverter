import sys

# from parser import GetFetchedTranscriptFromFile
from _dictionary import GetDutchWordEntry
from _csv_utils import TableIO
from _helper import PromptUserWordSelection, FormatDictionaryEntries
from _transcript import GetTranscriptString, ExtractListOfNewUniqueWords
from youtube_transcript_api import YouTubeTranscriptApi

# from youtube_transcript_api import FetchedTranscript
# from youtube_transcript_api import FetchedTranscriptSnippet
# from youtube_transcript_api.proxies import GenericProxyConfig
# from youtube_transcript_api.proxies import WebshareProxyConfig

FILE_NAME = "test.csv"

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

### user input
user_input = input("Please provide YT video ID or URL:").split("/watch?v=")
if len(user_input) == 1:
    video_id = user_input[0]
elif len(user_input) == 2:
    video_id = user_input[1]
else:
    video_id = None

### Hardcoded video ID
# video_id = "J2y1wVCD9hI"

### Get transcript from YouTube
if video_id:
    try:
        transcript_list = ytt_api.list(video_id)  # languages=['nl', 'en']
        nl_transcript = transcript_list.find_transcript(["nl"])
        original_transcript = nl_transcript.fetch()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit()
else:
    print("Error: Missing video ID. Exiting script.")
    sys.exit()

# original_transcript = GetFetchedTranscriptFromFile()
raw_transcript = GetTranscriptString(original_transcript)
# pprint(raw_transcript, indent=2, width=40)

new_words = ExtractListOfNewUniqueWords(raw_transcript, FILE_NAME)
user_approved_words = PromptUserWordSelection(new_words)
if user_approved_words:
    word_entries = [GetDutchWordEntry(word) for word in user_approved_words]
else:
    print("No words approved for import. Exiting script.")
    sys.exit()

valid_word_entries = []
invalid_word_entries = []
for entry in word_entries:
    if len(entry["senses"]):
        valid_word_entries.append(entry)
    else:
        invalid_word_entries.append(entry)

if invalid_word_entries:
    print(
        f"⚠ Following words were not found in the dictionary and will not be added to the deck: {[entry['word'] for entry in invalid_word_entries]}\n"
    )

formatted_entries = FormatDictionaryEntries(valid_word_entries)
table = TableIO("test.csv")
table.writeRows(formatted_entries)
