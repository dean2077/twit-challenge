#!/usr/bin/env python3
"""
Write a Python program that monitors a Twitter account.

    The program must output text from new tweets to stdout.
    The program must output the 5 most recent tweets right after execution, then it must check for new tweets
    (and display them) every 10 mins.
    The Twitter handle will be provided as a command-line argument by the user starting the program
    Make sure to use scraping or APIs that do not require user authentication or a Twitter developer account.
    Must not use open source libraries such as Twint, Tweepy to do the heavy lifting

    Bonus round #1: Modify your Python program to add a simple API to dump all the tweets collected so far in JSON
    format via a simple curl command.
"""
import os
import argparse
import logging
import time
import json
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

logger = logging.getLogger(__name__)


class Tweet:
    def __init__(self, username, tweet_url):
        # tweet basic data
        self.username = username
        self.tweet_url = tweet_url
        # create a file of tweets per user
        self.output_path = os.path.abspath(os.path.join(os.getcwd(), username + '-tweets.json'))
        # create a dictionary of tweets based on the username
        self.tweet_dict = {
            "tweet_username": username,
            "tweet_url": tweet_url,
            "tweets": [
                # {
                #     "timestamp": timestamp,
                #     "tweet_text": text
                # }
            ]
        }

    def dump_to_file(self, output_path):
        """
        Write tweet data to an json output file
        """
        if os.path.exists(os.path.abspath(output_path)):
            # if file already exists we only want to add the new tweets
            # thus we need to load in current data and check
            with open(output_path) as input_file:
                data = json.load(input_file)
            for tweet in data['tweets']:
                if tweet not in self.tweet_dict['tweets']:
                    # add the new tweet to tweet_dict
                    self.add_tweet(tweet['timestamp'], tweet['text'])

        # Write the output
        with open(output_path, 'w') as output_file:
            json.dump(self.tweet_dict, output_file, indent=4)

    def add_tweet(self, timestamp, tweet_text):
        self.tweet_dict['tweets'].append(
            {'timestamp': timestamp, 'tweet_text': tweet_text}
        )


def css_method(username, check, curl):
    """
    Using selenium to get tweets
    param username: username of the person to return tweets from
    param check: boolean, if true will check for new tweets every 10 minutes
    param curl: dump tweets to a file
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
    actions = ActionChains(driver)
    time.sleep(5)

    tweet_search = "div:nth-child({}) > div > div > article > div > div > div > div.css-1dbjc4n.r-18u37iz > " \
                   "div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-1mi0q7o > div:nth-child(2) > div:nth-child(1) > div"
    time_search = "div:nth-child({}) > div > div > article > div > div > div > div.css-1dbjc4n.r-18u37iz > " \
                  "div.css-1dbjc4n.r-1iusvr4.r-16y2uox.r-1777fci.r-1mi0q7o > div:nth-child(1) > div > div > " \
                  "div.css-1dbjc4n.r-1d09ksm.r-18u37iz.r-1wbh5a2 > a > time"

    tweets = []
    i = 0
    tweet_count = 0
    # init tweet_obj
    tweet_obj = Tweet(username=username, tweet_url=api_url)
    while True:
        i += 1
        if i is 10:
            # Give up after 10 tries to get 5 tweets
            break
        try:
            tweet = driver.find_element(By.CSS_SELECTOR, tweet_search.format(i))
            timestamp = driver.find_element(By.CSS_SELECTOR, time_search.format(i))
            # if curl create tweet_obj and dump to file
            if curl:
                tweet_obj.add_tweet(timestamp.text, tweet.text)
            # print to stdout no matter what
            print(f'--------------------- tweet number: {i} is: --------------------\n'
                  f' {tweet.text}\n'
                  f'--------------------- end tweet number {i} ---------------------\n')
        except NoSuchElementException:
            # couldn't find the tweet, continue
            # I believe this is an issue with the page not being scrolled down enough
            print(f"couldn't find tweet number {i}, may have been deleted")
            continue
        tweets.append(tweet.text)
        tweet_count += 1
        # Found the number of tweets we were after
        if tweet_count is 5:
            break
        time.sleep(2)
        # Force the page to move down to the current tweet
        actions.move_to_element(tweet).perform()

    if check:
        while True:
            # Sleep for 10 mintues and then check for a new tweet
            print('Waiting for 10minutes and then checking for a new tweet\n')
            print('Press crtl+c to cancel')
            time.sleep(600)
            tweet = driver.find_element(By.CSS_SELECTOR, tweet_search.format(1))
            timestamp = driver.find_element(By.CSS_SELECTOR, time_search.format(1))
            if tweet.text not in tweets:
                if curl:
                    tweet_obj.add_tweet(timestamp.text, tweet.text)
                print(f'--------------------- new tweet -------------------------\n'
                      f' {tweet.text}\n'
                      f'--------------------- end new tweet ---------------------\n')
                tweets.append(tweet.text)

    driver.close()
    if curl:
        tweet_obj.dump_to_file(tweet_obj.output_path)
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
    parser.add_argument(
        "--curl",
        action='store_true',
        dest="curl",
        help="use this command to dump tweets to an output file"
    )
    args = parser.parse_args()
    css_method(args.username, args.check, args.curl)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
