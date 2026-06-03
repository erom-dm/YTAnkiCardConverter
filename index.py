import sys

from parser import GetFetchedTranscriptFromFile
from _dictionary import GetDutchWordEntry
from _translation import translate_text
import argparse
from _csv_utils import TableIO
from _helper import PromptUserWordSelection, FormatDictionaryEntries
from _transcript import GetTranscriptString, ExtractListOfNewUniqueWords
from youtube_transcript_api import YouTubeTranscriptApi

# from youtube_transcript_api import FetchedTranscript
# from youtube_transcript_api import FetchedTranscriptSnippet
# from youtube_transcript_api.proxies import GenericProxyConfig
# from youtube_transcript_api.proxies import WebshareProxyConfig

FILE_NAME = "test.csv"
DEFAULT_SOURCE_LANGUAGE = "nl"

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

parser = argparse.ArgumentParser(
    description="A script that creates Anki deck from word inputs or Youtube transcripts"
)
parser.add_argument(
    "-l",
    "--language",
    type=str,
    default=DEFAULT_SOURCE_LANGUAGE,
    help="A language you're translating from in in ISO 639-1 code ('nl', 'fr', etc.)",
)
parser.add_argument(
    "-d",
    "--direct",
    action="store_true",
    help="A direct word imput mode, that bypasses YouTube transcript download and word selection",
)
parser.add_argument(
    "-t",
    "--test",
    action="store_true",
    help="Test mode, that uses mock YouTube transcript response stored in file",
)
args = parser.parse_args()

### Hardcoded video ID
# video_id = "J2y1wVCD9hI"
# pprint(raw_transcript_string, indent=2, width=40)

if args.direct:
    translation_input = input("Please provide a word or a phrase: ")
elif args.test:
    translation_input = GetTranscriptString(GetFetchedTranscriptFromFile())
else:
    user_input = input("Please provide YT video ID or URL:").split("/watch?v=")
    if len(user_input) == 1:
        video_id = user_input[0]
    elif len(user_input) == 2:
        video_id = user_input[1]
    else:
        video_id = None
    ### Get transcript from YouTube
    if video_id:
        try:
            transcript_list = ytt_api.list(video_id)  # languages=['nl', 'en']
            nl_transcript = transcript_list.find_transcript([args.language])
            transcript = nl_transcript.fetch()
            translation_input = GetTranscriptString(transcript)
        except Exception as e:
            print(f"An error occurred: {e}")
            sys.exit()
        else:
            print("Error: Missing video ID. Exiting script.")
            sys.exit()

new_words = ExtractListOfNewUniqueWords(translation_input, FILE_NAME)
if not len(new_words):
    print("All inputs already exist in the table. Exiting script.")
    sys.exit()

if args.direct:
    user_approved_words = new_words
else:
    user_approved_words = PromptUserWordSelection(new_words)

if user_approved_words:
    google_translations = translate_text(user_approved_words, args.language)
    word_entries = [GetDutchWordEntry(word) for word in user_approved_words]
else:
    print("No words approved for import. Exiting script.")
    sys.exit()

valid_word_entries = []
invalid_word_entries = []
for entry in word_entries:
    if len(entry["senses"]):
        g_translation = next(
            (
                el["translatedText"]
                for el in google_translations
                if el["input"] == entry["word"]
            ),
            None,
        )
        valid_word_entries.append({**entry, "google_translation": g_translation})
    else:
        invalid_word_entries.append(entry)

if invalid_word_entries:
    print(
        f"⚠ Following words were not found in the dictionary and will not be added to the deck: {[entry['word'] for entry in invalid_word_entries]}\n"
    )

formatted_entries = FormatDictionaryEntries(valid_word_entries)
table = TableIO("test.csv")
table.writeRows(formatted_entries)
