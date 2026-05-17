import questionary

FIELD_NAMES = [
    "word",
    "part of speech",
    "plural",
    "definitions",
    "examples",
    "source",
]


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


def FormatDictionaryEntries(entries: list[dict]) -> list[dict[str:str]]:
    formatted_entries = []
    for entry in entries:
        definitions = []
        examples = []
        for sense in entry.get("senses"):
            definitions.append(sense.get("definition", ""))
            examples.append(sense.get("examples", ""))

        formatted_entry = dict.fromkeys(FIELD_NAMES, "")
        formatted_entry["word"] = entry.get("word", "")
        formatted_entry["part of speech"] = entry.get("partOfSpeech", "")
        formatted_entry["plural"] = [
            f"{el.get('word', '')} ({el.get('tags', '')})"
            for el in entry.get("plural", "")
        ]
        formatted_entry["definitions"] = definitions
        formatted_entry["examples"] = examples
        formatted_entry["source"] = entry.get("source", "")
        formatted_entries.append(formatted_entry)
    return formatted_entries
