# TODO: use request session
# TODO: read from already saved file

from argparse import ArgumentParser
from bs4 import BeautifulSoup
import requests

language_dict = {
    1: 'arabic',
    2: 'german',
    3: 'english',
    4: 'spanish',
    5: 'french',
    6: 'hebrew',
    7: 'japanese',
    8: 'dutch',
    9: 'polish',
    10: 'portuguese',
    11: 'romanian',
    12: 'russian',
    13: 'turkish'
}


def main(from_lang, to_lang, word):
    # print("Hello, you're welcome to the translator. Translator supports:")
    # i = 1
    # for _, values in language_dict.items():
    #     print(f"{i}. {values.capitalize()}")
    #     i += 1

    # from_lang = int(input("Type the number of your language:\n"))
    # to_lang = int(input("Type the number of language you want to translate to"
    #                     "or '0' to translate to all languages:\n"))
    # word = input("Type the word you want to translate:\n")

    # from_lang = language_dict[from_lang]

    if to_lang == "all":
        for _, lang in language_dict.items():
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
        # to_lang = language_dict[to_lang]x

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
    r = requests.get(request_url, headers=headers)
    if not r:
        print(f"Please visit: {request_url}")
        return

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
    main(args.from_lang, args.to_lang, args.word)
