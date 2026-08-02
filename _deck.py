import csv
import os

import genanki
from gtts import gTTS
from slugify import slugify

FIELDS = [
    {"name": "Word"},
    {"name": "POS"},  # Part of Speech
    {"name": "Translation"},
    {"name": "Plural"},
    {"name": "Definitions"},
    {"name": "Examples"},
    {"name": "Source"},
    {"name": "Audio"},  # Anki format: [sound:filename.mp3]
]

CSS = """
.card {
    font-family: system-ui, -apple-system, sans-serif;
    font-size: 18px;
    text-align: center;
    color: #2c3e50;
    background-color: #f8f9fa;
    padding: 20px;
}
.word { font-size: 36px; font-weight: bold; color: #2980b9; }
.pos { font-style: italic; color: #91a2a3; font-size: 16px; margin-bottom: 8px; }
.translation { font-size: 32px; color: #2980b9; font-weight: 600; margin-bottom: 8px; }
.plural { font-size: 16px; color: #e67e22; margin-top: 4px; text-align: left; }
.section-title { font-weight: bold; font-size: 12px; text-transform: uppercase; color: #95a5a6; margin-top: 15px; }
.definition, .example { font-size: 18px; color: #91a2a3; margin-top: 4px; line-height: 1.4; text-align: left; }
.source { font-size: 11px; color: #bdc3c7; margin-top: 25px; text-align: left; }
hr { border: 0; height: 1px; background: #00ecfa; margin: 15px 0; }
"""

# Bidirectional Model 1
MODEL_STANDARD_BIDIRECTIONAL = genanki.Model(
    1087777856,  # Unique Model ID
    "Standard Bidirectional Vocab",
    fields=FIELDS,
    templates=[
        # --- CARD 1: Word -> Translation (Recognition) ---
        {
            "name": "Recognition (Word -> Translation)",
            "qfmt": """
                <div class="word">{{Word}}</div>
                 {{#Examples}}
                    <div class="section-title">Example</div>
                    <div class="example">{{Examples}}</div>
                {{/Examples}}
                <div>{{Audio}}</div>
            """,
            "afmt": """
                <div class="word">{{Word}}</div>
                {{#Examples}}
                    <div class="section-title">Example</div>
                    <div class="example">{{Examples}}</div>
                {{/Examples}}
                <div>{{Audio}}</div>
                <hr>
                <div class="translation">{{Translation}}</div>
                {{#POS}}<div class="pos">({{POS}})</div>{{/POS}}
                {{#Plural}}<div class="plural"><b>Plural:</b> {{Plural}}</div>{{/Plural}}
                
                {{#Definitions}}
                    <div class="section-title">Definition</div>
                    <div class="definition">{{Definitions}}</div>
                {{/Definitions}}
                
                {{#Source}}<div class="source">Src: {{Source}}</div>{{/Source}}
            """,
        },
        # --- CARD 2: Translation -> Word (Production) ---
        {
            "name": "Production (Translation -> Word)",
            "qfmt": """
                <div class="translation">{{Translation}}</div>
                {{#POS}}<div class="pos">({{POS}})</div>{{/POS}}
                {{#Definitions}}
                    <div class="section-title">Hint / Definition</div>
                    <div class="definition">{{Definitions}}</div>
                {{/Definitions}}
            """,
            "afmt": """
                {{#POS}}<div class="pos">({{POS}})</div>{{/POS}}
                <div class="translation">{{Translation}}</div>
                <hr>
                <div class="word">{{Word}}</div>
                <div>{{Audio}}</div>
                {{#Plural}}<div class="plural"><b>Plural:</b> {{Plural}}</div>{{/Plural}}
                
                {{#Examples}}
                    <div class="section-title">Example</div>
                    <div class="example">{{Examples}}</div>
                {{/Examples}}
                
                {{#Source}}<div class="source">Src: {{Source}}</div>{{/Source}}
            """,
        },
    ],
    css=CSS,
)


def FillAnkiDeck(filename: str, language: str):
    deck = genanki.Deck(
        1837671339,  # Unique id
        filename,
    )

    media_files = []
    with open(filename + ".csv", mode="r", encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            fields = [
                row["word"],
                row["part of speech"],
                row["translation"],
                row["plural"],
                row["definitions"],
                row["examples"],
                row["source"],
            ]

            if row["word"]:
                audio_filename = slugify(row["word"]) + ".mp3"
                if not os.path.exists("./audio/" + audio_filename):
                    tts = gTTS(text=row["word"], lang=language)
                    tts.save("./audio/" + audio_filename)

                media_files.append("./audio/" + audio_filename)
                fields.append(f"[sound:{audio_filename}]")
            else:
                fields.append("")

            deck.add_note(
                genanki.Note(model=MODEL_STANDARD_BIDIRECTIONAL, fields=fields)
            )

        genanki.Package(deck, media_files=media_files).write_to_file(
            "./" + filename + ".apkg"
        )
