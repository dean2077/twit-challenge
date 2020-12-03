#!/usr/bin/env python3
"""
Write a Python program that monitors a Twitter account.

    The program must output text from new tweets to stdout.
    The program must output the 5 most recent tweets right after execution, then it must check for new tweets (and display them) every 10 mins.
    The Twitter handle will be provided as a command-line argument by the user starting the program
    Make sure to use scraping or APIs that do not require user authentication or a Twitter developer account.
    Must not use open source libraries such as Twint, Tweepy to do the heavy lifting
"""
import os
import argparse
import logging
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

logger = logging.getLogger(__name__)


def css_method(username, check):
    """
    Using selenium to get tweets
    param username: username of the person to return tweets from
    param check: boolean, if true will check for new tweets every 10 minutes
    """

    options = webdriver.ChromeOptions()
    options.headless = True
    chrome_driver_path = os.getenv(
        'ChromeDriver',
        default=r'C:\Users\User\Downloads\chromedriver_win32\chromedriver.exe'
    )
    driver = webdriver.Chrome(chrome_driver_path, options=options)
    api_url = "https://twitter.com/" + username
    driver.get(api_url)
    time.sleep(5)

    search = "div:nth-child({}) > div > div > article > div > div > div > div.css-1dbjc4n.r-18u37iz > " \
             "div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-1mi0q7o > div:nth-child(2) > div:nth-child(1)"

    tweets = []
    i = 0
    tweet_count = 0
    while True:
        i += 1
        if tweet_count is 5 or i is 10:
            # found the number of tweets we want
            # or i has gone too high
            break
        # Get first tweet, currently working

        try:
            tweet = driver.find_element(By.CSS_SELECTOR, search.format(i))
            print(f'---------------------tweet number: {i} is: --------------------\n'
                  f' {tweet.text}\n'
                  f'---------------------end tweet number {i} ---------------------\n')
        except NoSuchElementException:
            # couldn't find the tweet, decrement i and continue
            print(f"couldn't find tweet number {i}")
            continue
        tweets.append(tweet.text)
        tweet_count += 1

    if check:
        while True:
            # Sleep for 10 mintues and then check for a new tweet
            print('Waiting for 10minutes and then checking for a new tweet\n')
            print('Press crtl+c to cancel')
            time.sleep(600)
            tweet = driver.find_element(By.CSS_SELECTOR, search.format(1))
            if tweet.text not in tweets:
                print(f'--------------------- new tweet -------------------------\n'
                      f' {tweet.text}\n'
                      f'--------------------- end new tweet ---------------------\n')
                tweets.append(tweet.text)

    driver.close()
    print(f'Finished css_method, found a total of {len(tweets)} tweet(s)')


def main():
    """ Main entry point of the app """
    parser = argparse.ArgumentParser()

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument(
        "-U", "--username",
        action="store",
        dest="username",
        help="Username to search tweets for",
        required=True
    )
    parser.add_argument(
        "-C", "--check",
        action='store_true',
        dest="check",
        help="Check every 10mins for a new tweet"
    )

    args = parser.parse_args()

    css_method(args.username, args.check)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
