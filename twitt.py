import csv
import sys
import re
from HTMLParser import HTMLParser

def process(tweet):
    processed_tweet = encode_ascii(tweet)
    processed_tweet = remove_html_tags(processed_tweet)
    processed_tweet = replace_html_character_codes(processed_tweet)
    return processed_tweet
    
def encode_ascii(tweet):
    return tweet.decode('utf-8', 'ignore').encode('ascii', 'ignore')

def remove_html_tags(tweet):
    return re.sub(r'<[^>]+>', "", tweet)

def replace_html_character_codes(tweet):
    h = HTMLParser()
    return h.unescape(tweet)

if __name__ == "__main__":
    with open(sys.argv[1], 'rb') as twitter_csv:
        reader = csv.reader(twitter_csv)
        for row in reader:
            print(process(row[5]))
    print "Done!"
    
