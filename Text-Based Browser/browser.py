from argparse import ArgumentParser
from bs4 import BeautifulSoup
from colorama import init, Fore
import os
import requests
import sys


def main(save_dir: str):
    """
    Main entry point for the program

    Args:
        save_dir: directory for saved tabs. Save all the web pages that the user downloads.

    Returns:
        None
    """
    # initialize colorama
    init()
    # Pages that are saved in a text file
    saved_pages = {}
    if os.path.isdir(save_dir):
        for saved_page in os.listdir(save_dir):
            saved_pages[saved_page.split('.')[0]] = f"{save_dir}/{saved_page}"
    else:
        os.mkdir(save_dir)

    visited_pages = []
    last_page = None
    while True:
        url = input()
        if "." in url:
            # Add protocol if protocol is missing
            if len(url) < 8 or (url[:8] != "https://" and url[:8] != "https://"):
                url = "https://" + url
            r = requests.get(url)
            if not r:
                print("Error: Incorrect URL")
                continue
            content = parse_html(r.text)
            print(Fore.BLUE + content)
            # save the visited page
            # remove the protocol
            temp_lst = url.split("//")
            temp_lst = temp_lst[1].split(".")
            # TODO: Adjustments for links which have paths attached at the end like test.org/projects/79/439/implement#1
            temp_lst[-1] = "txt"
            file_name = ".".join(temp_lst)
            file_path = f"{save_dir}/{file_name}"
            if last_page:
                visited_pages.append(last_page)
            last_page = file_path
            # save as visited pages / update if already visited
            with open(file_path, 'w+', encoding="utf-8") as f:
                f.write(content)
                # key = file name without .txt extension
            saved_pages[file_name[:-4]] = file_path
        else:
            if url == 'exit':
                sys.exit(0)

            if url == 'back':
                if len(visited_pages) > 0:
                    with open(visited_pages.pop(), 'r', encoding='utf-8') as f:
                        content = f.read()
                    print(Fore.BLUE + content)
                continue

            try:
                with open(saved_pages[url], 'r', encoding='utf-8') as f:
                    content = f.read()
                print(Fore.BLUE + content)
                if last_page:
                    visited_pages.append(last_page)
                last_page = saved_pages[url]
            except KeyError:
                print("Error: Incorrect URL")


def parse_html(html_str: str) -> str:
    """
    Parses  html

    Args:
    html_str: html string

    Returns:
        str: parsed html without html tags
    """
    soup = BeautifulSoup(html_str, 'html.parser')
    return soup.get_text()


if __name__ == '__main__':
    # Entry point from command line
    parser = ArgumentParser()
    parser.add_argument('save_dir', help="directory to save web pages")
    args = parser.parse_args()
    main(args.save_dir)
