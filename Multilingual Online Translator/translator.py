# TODO: use request session
# TODO: read from already saved file

from argparse import ArgumentParser
from bs4 import BeautifulSoup
import requests
import sys

languages = {'arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese', 'dutch', 'polish', 'portuguese', 'romanian', 'russian', 'turkish'}


def main(from_lang, to_lang, word):
    if from_lang not in languages:
        print(f"Sorry, the program doesn't support {from_lang}")
        return
    elif to_lang not in languages and to_lang != "all":
        print(f"Sorry, the program doesn't support {to_lang}")
        return

    if to_lang == "all":
        for lang in languages:
            if lang == from_lang:
                continue
            translated_words, examples, example_translations = translate(from_lang, lang, word, 1)
            with open(f"{word}.txt", 'a+', encoding='utf-8') as f:
                f.write(f"{lang.capitalize()} Translation:")
                f.write(f"\n{translated_words[0]}")
                f.write(f"\n\n{lang.capitalize()} Example:")
                f.write(f"\n{examples[0]}")
                f.write(f"\n{example_translations[0]}\n\n\n")

    else:
        translated_words, examples, example_translations = translate(from_lang, to_lang, word)

        with open(f"{word}.txt", 'a+', encoding='utf-8') as f:
            f.write(f"{to_lang.capitalize()} Translation:")
            for translated_word in translated_words:
                f.writelines(f"\n{translated_word}")
            f.write(f"\n\n{to_lang.capitalize()} Example:")
            for example, example_translation in zip(examples, example_translations):
                f.write(f"\n{example}")
                f.write(f"\n{example_translation}\n")

    with open(f"{word}.txt", 'r', encoding='utf-8') as f:
        content = f.read()
    print(content)


def translate(from_lang: str, to_lang: str, word: str, result_limit=None) -> (list, list, list):
    request_url = f"https://context.reverso.net/translation/{from_lang}-{to_lang}/{word}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        r = requests.get(request_url, headers=headers)
    except requests.ConnectionError:
        print("Something wrong with your internet connection")
        sys.exit(1)

    soup = BeautifulSoup(r.content, 'html.parser')
    # translated words
    translated_words = get_text_only(soup.find_all('a', "translation"))
    # fix for first translated word being translations
    translated_words.pop(0)
    # example sentences in `from` language
    examples = get_text_only(soup.find_all('div', 'src ltr'))
    # translated sentences in `to` language
    if to_lang == 'arabic':
        example_translations = get_text_only(soup.find_all('div', 'trg rtl arabic'))
    elif to_lang == 'hebrew':
        example_translations = get_text_only(soup.find_all('div', 'trg rtl'))
    else:
        example_translations = get_text_only(soup.find_all('div', 'trg ltr'))

    if result_limit:
        translated_words = translated_words[:result_limit]
        examples = examples[:result_limit]
        example_translations = example_translations[:result_limit]

    if len(translated_words) == 0:
        print(f"Sorry, unable to find {word}")
        sys.exit(1)

    return translated_words, examples, example_translations


def get_text_only(raw_texts: list):
    refined_texts = []
    for raw_text in raw_texts:
        refined_texts.append(raw_text.text.strip())
    return refined_texts


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("from_lang", help="Language to translate from")
    parser.add_argument("to_lang", help="Language to translate to")
    parser.add_argument("word", help="Word to translate")
    args = parser.parse_args()
    main(args.from_lang.lower(), args.to_lang.lower(), args.word)
