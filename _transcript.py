import string
from youtube_transcript_api import FetchedTranscript
from _csv_utils import TableIO


def GetTranscriptString(transcript: FetchedTranscript):
    """
    Concatenate all snippets from FetchedTranscript instance and get whole transcript in a signle string
    """
    whole_text = ""
    end_of_line_chars = [".", "?", "!", "]", ")"]
    for snippet in transcript:
        if len(whole_text) and whole_text[-1] in end_of_line_chars:
            whole_text += " " + snippet.text
        else:
            whole_text += snippet.text

    return whole_text


def ExtractListOfNewUniqueWords(transcript: str, file_name: str) -> set[str]:
    """
    Get a list of unique words from a transcript. Then check against .csv file contents, and filter out repeating words.
    """
    clean_transcript = "".join(
        [char for char in transcript if char not in string.punctuation]
    )
    individual_words = clean_transcript.split(" ")
    unique_words_from_transcript = set(
        [word.lower() for word in individual_words if word.isalpha()]
    )
    table = TableIO(file_name)
    table_words = [entry.get("word") for entry in table.readRows()]
    unique_and_filtered_words = [
        word for word in unique_words_from_transcript if word not in table_words
    ]
    return sorted(unique_and_filtered_words)
