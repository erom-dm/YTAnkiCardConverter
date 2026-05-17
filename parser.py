import ast
import re
from pprint import pprint
from typing import List, Iterator, Dict
from dataclasses import dataclass, asdict
from youtube_transcript_api import FetchedTranscript
from youtube_transcript_api import FetchedTranscriptSnippet

# --- The Parsing Logic ---


def GetFetchedTranscriptFromFile():
    # 1. Read the raw text from your file
    with open("sample.txt", "r", encoding="utf-8") as f:
        raw_string = f.read()

    # 2. Use Regex to strip out the class names so it becomes a valid Python dict/list literal
    cleaned_string = re.sub(r"FetchedTranscript\s*\(", "{", raw_string)
    cleaned_string = re.sub(r"FetchedTranscriptSnippet\s*\(", "{", cleaned_string)
    cleaned_string = (
        cleaned_string.replace("),", "},").replace(")]", "}]").replace(")", "}")
    )
    cleaned_string = re.sub(
        r"(\w+)\s*=", r"'\1':", cleaned_string
    )  # Turn keys like video_id= into 'video_id':

    # 3. Safely evaluate the string into a standard Python dictionary
    data_dict = ast.literal_eval(cleaned_string)

    # 4. Reconstruct the dataclass instances from the dictionary data
    snippets = [FetchedTranscriptSnippet(**s) for s in data_dict["snippets"]]
    return FetchedTranscript(
        snippets=snippets,
        video_id=data_dict["video_id"],
        language=data_dict["language"],
        language_code=data_dict["language_code"],
        is_generated=data_dict["is_generated"],
    )


# transcript_instance = GetFetchedTranscriptFromFile()

# --- Verification ---
# print(type(transcript_instance))  # Output: <class '__main__.FetchedTranscript'>
# print(transcript_instance.video_id)  # Output: 1ZDekaw6vwg
# print(transcript_instance.snippets[0].text)
# pprint(transcript_instance, indent=2, width=40)
