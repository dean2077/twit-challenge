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
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


def css_method(username):

    search = ".r-1ljd8xs > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(3) > section:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > article:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > span:nth-child(1)"

    options = webdriver.ChromeOptions()
    options.headless = True
    driver = webdriver.Chrome(r'C:\Users\User\Downloads\chromedriver_win32\chromedriver.exe', options=options)
    api_url = "https://twitter.com/" + username
    driver.get(api_url)
    time.sleep(5)

    # Get first tweet, currently working
    # search = "div:nth-child(1) > div > div > article > div > div > div > div.css-1dbjc4n.r-18u37iz > " \
    #          "div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-1mi0q7o > div:nth-child(2) > div:nth-child(1)"
    # tweet = driver.find_element(By.CSS_SELECTOR, search)
    # print(f'---------------------first tweet is:---------------------\n'
    #       f' {tweet.text}'
    #       f'\n---------------------end first tweet---------------------')

    tweets = []
    for i in range(1, 6):
        # Get first tweet, currently working
        search = f"div:nth-child({i}) > div > div > article > div > div > div > div.css-1dbjc4n.r-18u37iz > " \
                 "div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-1mi0q7o > div:nth-child(2) > div:nth-child(1)"
        tweet = driver.find_element(By.CSS_SELECTOR, search)
        print(f'---------------------tweet number: {i} is: --------------------\n'
              f' {tweet.text}\n'
              f'---------------------end tweet number {i} ---------------------\n')

    #     search = f"div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-1mi0q7o > div:nth-child(2) > div:nth-child(1)"
    #     tweet = driver.find_element(By.CSS_SELECTOR, search)
    #     print(f'{i} tweet is: {tweet.text}')
    #     tweets.append(tweet)

    driver.close()
    print('done css method')


def main(args):
    """ Main entry point of the app """
    logging.info("hello world")
    logging.info(args)

    css_method(args.username)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()

    # Optional argument which requires a parameter (eg. -d test)
    parser.add_argument("-U", "--username", action="store", dest="username")

    args = parser.parse_args()
    main(args)
