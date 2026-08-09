import argparse
import sys

from youtube_transcript_api import YouTubeTranscriptApi

from _csv_utils import TableIO
from _deck import FillAnkiDeck
from _dictionary import GetDutchWordEntry
from _helper import FormatDictionaryEntries, PromptUserWordSelection
from _transcript import ExtractListOfNewUniqueWords, GetTranscriptString
from _translation import translate_text
from parser import GetFetchedTranscriptFromFile

# from youtube_transcript_api import FetchedTranscript
# from youtube_transcript_api import FetchedTranscriptSnippet
# from youtube_transcript_api.proxies import GenericProxyConfig
# from youtube_transcript_api.proxies import WebshareProxyConfig

FILE_NAME = "deck_1"
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
    "-n",
    "--name",
    type=str,
    default=FILE_NAME,
    help="File name for both csv and apkg output (no extension)",
)
parser.add_argument(
    "-s",
    "--single",
    action="store_true",
    help="A single word input mode, that bypasses YouTube transcript download and word selection",
)
parser.add_argument(
    "-d",
    "--direct",
    type=str,
    help="Provide a single word/phrase as an argument",
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

if args.single:
    translation_input = input("Please provide a word or a phrase: ")
elif args.direct:
    translation_input = args.direct
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

if args.single or args.direct:
    new_words = [translation_input]
else:
    new_words = ExtractListOfNewUniqueWords(translation_input, args.name)
if not len(new_words):
    print("All inputs already exist in the table. Exiting script.")
    sys.exit()

if args.single or args.direct:
    user_approved_words = new_words
else:
    user_approved_words = PromptUserWordSelection(new_words)

if user_approved_words:
    google_translations = translate_text(user_approved_words, args.language)
    word_entries = [
        GetDutchWordEntry(word, args, args.language) for word in user_approved_words
    ]
else:
    print("No words approved for import. Exiting script.")
    sys.exit()

valid_word_entries = []
invalid_word_entries = []
for entry in word_entries:
    g_translation = next(
        (
            el["translatedText"]
            for el in google_translations
            if el["input"] == entry["word"]
        ),
        None,
    )
    if args.single or args.direct or len(entry["senses"]):
        valid_word_entries.append({**entry, "google_translation": g_translation})
    else:
        invalid_word_entries.append(entry)

if invalid_word_entries:
    print(
        f"⚠ Following words were not found in the dictionary and will not be added to the deck: {[entry['word'] for entry in invalid_word_entries]}\n"
    )

formatted_entries = FormatDictionaryEntries(valid_word_entries)
table = TableIO(args.name + ".csv")
table.writeRows(formatted_entries)

FillAnkiDeck(args.name, args.language)
