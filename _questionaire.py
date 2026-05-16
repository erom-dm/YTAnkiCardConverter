import questionary

def PromptUserWordSelection(word_list):
    selected_words = questionary.checkbox('Select new words you want to import:\n', choices=word_list, use_jk_keys=False, use_search_filter=True).ask()
    if selected_words is None:
        print("Selection cancelled.")
    return selected_words
