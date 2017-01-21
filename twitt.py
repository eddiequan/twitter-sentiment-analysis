import csv
import sys
import re
from HTMLParser import HTMLParser

def process(tweet):
    processed_tweet = encode_ascii(tweet)
    processed_tweet = remove_html_tags(processed_tweet)
    processed_tweet = replace_html_character_codes(processed_tweet)
    processed_tweet = remove_urls(processed_tweet)
    processed_tweet = chomp_usernames(processed_tweet)
    return processed_tweet
    
def encode_ascii(tweet):
    return tweet.decode('utf-8', 'ignore').encode('ascii', 'ignore')

def remove_html_tags(tweet):
    return re.sub(r'<[^>]+>', "", tweet)

def replace_html_character_codes(tweet):
    h = HTMLParser()
    return h.unescape(tweet)
    
def remove_urls(tweet):
    # regex pattern copped from https://gist.github.com/uogbuji/705383
    URL_REGEX = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
    return re.sub(URL_REGEX, "", tweet)
    
def chomp_usernames(tweet):
    TWITTER_HANDLE_REGEX = '(?<=^|(?<=[^a-zA-Z0-9-\.]))@([A-Za-z0-9_]+)'
    usernames = re.findall(TWITTER_HANDLE_REGEX, tweet)
    
    chomped_tweet = tweet
    for username in usernames:
        chomped_tweet = chomped_tweet.replace("@" + username, username)
    return chomped_tweet
    

if __name__ == "__main__":
    with open(sys.argv[1], 'rb') as twitter_csv:
        reader = csv.reader(twitter_csv)
        for row in reader:
            print(process(row[5]))
    print "Done!"
    
