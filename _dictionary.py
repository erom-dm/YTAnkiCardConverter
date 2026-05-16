import requests
from pprint import pprint
import urllib.parse

URL = 'https://freedictionaryapi.com/api/v1/entries'
TRANSLATION = '?translations=true'

def GetDutchWordEntry(word: str, language: str = 'nl'):
    """
    Requests Dutch word entry from freedictionary. 1000 requests per day rate limit.
    """
    try:
        formattedURL = f"{URL}/{language}/{urllib.parse.quote(word)}{TRANSLATION}"
        response = requests.get(formattedURL)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

    entries = data.get('entries')
    if (len(entries)):
        entry = entries[0]
        return {
            "word": data.get('word'),
            "partOfSpeech": entry.get('partOfSpeech'),
            "plural": [item for item in entry.get('forms') if "plural" in item.get('tags')],
            "senses": [{"definition": item.get('definition'), "examples": item.get('examples')} for item in entry.get('senses')],
            "source": data.get('source').get('url')
        }
    else:
        return {
            "word": data.get('word'),
            "senses": []
        }
