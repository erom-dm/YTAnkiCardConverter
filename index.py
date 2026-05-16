import sys
import string
from pprint import pprint
from parser import GetFetchedTranscriptFromFile
from _dictionary import GetDutchWordEntry
from _questionaire import PromptUserWordSelection
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api import FetchedTranscript
from youtube_transcript_api import FetchedTranscriptSnippet
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

### Hardcoded video ID
# video_id = "J2y1wVCD9hI"

# if (video_id):
#     try:
#         transcript_list = ytt_api.list(video_id) #languages=['nl', 'en']
#         nl_transcript = transcript_list.find_transcript(['nl'])
#         original_transcript = nl_transcript.fetch()
#         translated_transcript = nl_transcript.translate('en').fetch()
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         sys.exit()
# else:
#     print("Error: Missing video ID. Exiting script")
#     sys.exit()

original_transcript = GetFetchedTranscriptFromFile()

def GetTranscriptString(transcript: FetchedTranscript):
    """
    Concatenate all snippets from FetchedTranscript instance and get whole transcript in a signle string
    """
    whole_text = ''
    end_of_line_chars = ['.', '?', '!', ']', ')']
    for snippet in transcript:
        if (len(whole_text) and whole_text[-1] in end_of_line_chars):
            whole_text += " " + snippet.text
        else:
            whole_text += snippet.text

    return whole_text

raw_transcript = GetTranscriptString(original_transcript)
# pprint(raw_transcript, indent=2, width=40)

def ExtractListOfUniqueWords(transcript: str):
    """
    Get a list of unique words from a transcript. 
    """
    clean_transcript = "".join([char for char in transcript if char not in string.punctuation])
    individual_words = clean_transcript.split(' ')
    return sorted(set([word.lower() for word in individual_words if word.isalpha()]))

unique_words = ExtractListOfUniqueWords(raw_transcript)
user_approved_words = PromptUserWordSelection(unique_words)
word_entries = [GetDutchWordEntry(word) for word in user_approved_words]
valid_word_entries = []
invalid_word_entries = []
for entry in word_entries:
    if len(entry["senses"]):
        valid_word_entries.append(entry)
    else:
        invalid_word_entries.append(entry)

print("Valid words:")
print(valid_word_entries)
print("Words not found:")
print(invalid_word_entries)

### remove all 

### Translations
# print(' ===== English auto-translated transcript:')
# print(f"  Number of snippets: {len(translated_transcript)}")
# for snippet in translated_transcript:
#     pprint(snippet.text, indent=2, width=40)