from google.cloud import translate_v2 as translate


def translate_text(
    text: str | list[str], source_language: str, target_language: str = "en"
):
    """
    text: string or list of strings to translate
    source_language: language code in ISO 639-1 code
    target_language: language code in ISO 639-1 code
    """
    translate_client = translate.Client()
    result = translate_client.translate(
        text,
        source_language=source_language,
        target_language=target_language,
        format_="text",
    )

    return result
