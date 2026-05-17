import questionary

FIELD_NAMES = ["word", "part of speech", "plural", "definitions", "examples", "source"]


def PromptUserWordSelection(word_list: list[str]) -> list[str] | None:
    """
    Prompts user to select words for import with interactive questionaire
    """
    selected_words = questionary.checkbox(
        "Select new words you want to import:\n",
        choices=word_list,
        use_jk_keys=False,
        use_search_filter=True,
    ).ask()
    if selected_words is None:
        print("Selection cancelled.")
    return selected_words


# def FormatDictionaryEntries(entries: list[dict]) -> list[dict[str:str]]:
#     foo


test_input = [
    {
        "word": "even",
        "partOfSpeech": "adverb",
        "plural": [],
        "senses": [
            {
                "definition": "shortly, briefly",
                "examples": ["Ik zal even voor u kijken."],
            },
            {
                "definition": "for a short period, for a while",
                "examples": [
                    "In de tweede helft van de 19e eeuw bloeide Vollenhove weer even op.^(nl:Vollenhove#Geschiedenis)"
                ],
            },
            {
                "definition": "for a moment; modal particle indicating that the speaker expects that something will require little time or effort.",
                "examples": ["Zou je even de deur voor me dicht willen doen?"],
            },
            {
                "definition": "just as, to the same degree (used with an adjective)",
                "examples": [
                    "In het midden van de vloer stond een tafel van wel vier meter hoog en een even grote stoel er bij."
                ],
            },
            {
                "definition": "(Netherlands) quite, rather",
                "examples": ["Die is even kwaad!"],
            },
        ],
        "source": "https://en.wiktionary.org/wiki/even",
    },
    {
        "word": "frisse",
        "partOfSpeech": "adjective",
        "plural": [],
        "senses": [{"definition": "inflection of fris:", "examples": []}],
        "source": "https://en.wiktionary.org/wiki/frisse",
    },
]
