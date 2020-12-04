#!/usr/bin/env python3
"""
Write a Python program that monitors a Twitter account.

    The program must output text from new tweets to stdout.
    The program must output the 5 most recent tweets right after execution, then it must check for new tweets (and display them) every 10 mins.
    The Twitter handle will be provided as a command-line argument by the user starting the program
    Make sure to use scraping or APIs that do not require user authentication or a Twitter developer account.
    Must not use open source libraries such as Twint, Tweepy to do the heavy lifting
"""

import argparse
import logging
from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession

logger = logging.getLogger(__name__)


def broken_links(username):
    import re
    import requests
    from requests_html import HTMLSession
    from urllib.parse import urlparse

    # Get Domain Name With urlparse
    url = "https://twitter.com/" + username
    parsed_url = urlparse(url)
    domain = parsed_url.scheme + "://" + parsed_url.netloc

    # Get URL
    session = HTMLSession()
    r = session.get(url)

    # Extract Links
    jlinks = r.html.xpath('/html/body/div/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div/div[2]/section/div/div/div[1]/div/div/article')

    print(f'jlinks are: {jlinks}')
    # Remove bad links and replace relative path for absolute path
    updated_links = []

    for link in jlinks:
        if re.search(".*@.*|.*javascript:.*|.*tel:.*", link):
            link = ""
        elif re.search("^(?!http).*", link):
            link = domain + link
            updated_links.append(link)
        else:
            updated_links.append(link)

    broken_links = []

    for link in updated_links:
        print(link)
        try:
            if requests.get(link, timeout=10).status_code != 200:
                broken_links.append(link)
        except requests.exceptions.RequestException as e:
            print(e)

    print(broken_links)


def more_adv_query(username):
    session = HTMLSession()
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Referer": f"https://twitter.com/{args.username}",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8",
        "X-Twitter-Active-User": "yes",
        "X-Requested-With": "XMLHttpRequest",
        "Accept-Language": "en-US",
    }
    url = "https://twitter.com/" + username
    response = session.get(url)
    if response.status_code == 200:
        try:
            json_response = response.json()
            print(json_response)
        # Wide Catch all mainly for JSONDecodeError
        except:
            with open("output2.html", "w", encoding="utf-8") as file:
                file.write(response.text)
    else:
        logger.error(f'{url} returned status code: {response.status_code}')


def basic_query(username):
    url = "https://twitter.com/" + username
    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text

    # Parse the html content
    soup = BeautifulSoup(html_content, "lxml")
    # print the parsed data of html
    # print(soup.prettify())

    # write the data to a file
    with open("output1.html", "w", encoding="utf-8") as file:
        file.write(str(soup))

    tweets = soup.find_all('li', 'js-stream-item')
    print(tweets)


def main(args):
    """ Main entry point of the app """
    logging.info("hello world")
    logging.info(args)
    basic_query(args.username)
    more_adv_query(args.username)
    broken_links(args.username)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-U", "--username", action="store", dest="username")

    args = parser.parse_args()
    main(args)

# from https://towardsdatascience.com/how-to-scrape-tweets-from-twitter-59287e20f0f1
# UPDATE: DUE TO CHANGES IN TWITTER’S API GETOLDTWEETS3 IS NO LONGER FUNCTIONING.
# TWEEPY AND SNSCRAPE ARE THE MOST PROMINENT SUBSTITUTES AS OF NOW.
# Both of which use OAUTH authentication
