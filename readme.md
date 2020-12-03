# twit-challenge

Goals of the challenge:

Write a Python program that monitors a Twitter account.

 - The program must output text from new tweets to stdout.
 - The program must output the 5 most recent tweets right after execution, then it must check for new tweets (and display them) every 10 mins.
 - The Twitter handle will be provided as a command-line argument by the user starting the program
 - Make sure to use scraping or APIs that do not require user authentication or a Twitter developer account.
 - Must not use open source libraries such as Twint, Tweepy to do the heavy lifting


## Requirements

- This project was built and tested with Python3.6
- run the command `pip install -r requirements` from root of the repo
- Requires chromedriver.exe obtainable from: https://chromedriver.chromium.org/
  - Once downloaded set the environment variable ChromeDriver to your path of the exe.
    - E.g. (in windows) `set ChromeDriver=<path_to_chromedriver.exe>`


## Usage

- `python twit-main.py --username textfiles`
  - find tweets for user textfiles
- `python twit-main.py --username textfiles --check`
  - find tweets for user textfiles and keep checking every 10 mins for new tweets