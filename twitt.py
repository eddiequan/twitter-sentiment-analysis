import csv
import sys
import re
import NLPlib
from HTMLParser import HTMLParser

PROPER_ABBREVIATIONS = ["Ala\.", "Ariz\.", "Assn\.", "Atty\.", "Aug\.", "Ave\.", "Bldg\.", "Blvd\.", "Calif\.", "Capt\.", "Cf\.", "Ch\.", "Co\.", "Col\.", "Colo\.", "Conn\.", "Corp\.", "DR\.", "Dec\.", "Dept\.", "Dist\.", "Dr\.", "Drs\.", "Ed\.", "Eq\.", "FEB\.", "Feb\.", "Fig\.", "Figs\.", "Fla\.", "Ga\.", "Gen\.", "Gov\.", "HON\.", "Ill\.", "Inc\.", "JR\.", "Jan\.", "Jr\.", "Kan\.", "Ky\.", "La\.", "Lt\.", "Ltd\.", "MR\.", "MRS\.", "Mar\.", "Mass\.", "Md\.", "Messrs\.", "Mich\.", "Minn\.", "Miss\.", "Mmes\.", "Mo\.", "Mr\.", "Mrs\.", "Mt\.", "NO\.", "No\.", "Nov\.", "Oct\.", "Okla\.", "Op\.", "Ore\.", "Pa\.", "Pp\.", "Prof\.", "Prop\.", "Rd\.", "Ref\.", "Rep\.", "Reps\.", "Rev\.", "Rte\.", "Sen\.", "Sept\.", "Sr\.", "St\.", "Stat\.", "Supt\.", "Tech\.", "Tex\.", "Va\.", "Vol\.", "Wash\."]

INLINE_ABBREVIATIONS = ["al\.", "av\.", "ave\.", "ca\.", "cc\.", "chap\.", "cm\.", "cu\.", "dia\.", "dr\.", "eqn\.", "etc\.", "fig\.", "figs\.", "ft\.", "gm\.", "hr\.", "in\.", "kc\.", "lb\.", "lbs\.", "mg\.", "ml\.", "mm\.", "mv\.", "nw\.", "oz\.", "pl\.", "pp\.", "sec\.", "sq\.", "st\.", "vs\.", "yr\."]

CLITICS = ["\'s", "\'re", "\'m", "\'ve", "\'d", "\'ll", "n\'t", "s\'"]

PROP_ABBREV_REGEX = "(" + ")|(".join(PROPER_ABBREVIATIONS) + ")"
INLINE_ABBREV_REGEX = "(" + ")|(".join(INLINE_ABBREVIATIONS) + ")"
CLITICS_REGEX = "(" + "|".join(CLITICS) + ")"


def process(tweet):
    processed_tweet = encode_ascii(tweet)
    processed_tweet = remove_html_tags(processed_tweet)
    processed_tweet = replace_html_character_codes(processed_tweet)
    processed_tweet = remove_urls(processed_tweet)
    processed_tweet = chomp_usernames(processed_tweet)
    processed_tweet = remove_hashtags(processed_tweet)
    processed_tweet = split_sentences(processed_tweet)
    processed_tweet = split_punctuation(processed_tweet)
    processed_tweet = split_clitics(processed_tweet)
    return processed_tweet
    
def encode_ascii(tweet):
    return tweet.decode('utf-8', 'ignore').encode('ascii', 'ignore')

def remove_html_tags(tweet):
    return re.sub(r'<[^>]+>', "", tweet)

def replace_html_character_codes(tweet):
    h = HTMLParser() # no need to instantiate each time?
    return h.unescape(tweet)
    
def remove_urls(tweet):
    # regex pattern copped from https://gist.github.com/uogbuji/705383
    URL_REGEX = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')
    return re.sub(URL_REGEX, "", tweet)
    
def split_punctuation(tweet):
    return re.sub(r"([\.!?]+)", r" \1", tweet)

# TODO: change to use regex?    
def chomp_usernames(tweet):
    TWITTER_HANDLE_REGEX = '(?<=^|(?<=[^a-zA-Z0-9-\.]))@([A-Za-z0-9_]+)'
    usernames = re.findall(TWITTER_HANDLE_REGEX, tweet)
    
    chomped_tweet = tweet
    for username in usernames:
        chomped_tweet = chomped_tweet.replace("@" + username, username)
    return chomped_tweet
    
# TODO: change to use regex?
def remove_hashtags(tweet):
    hashtags = [word for word in tweet.split() if word[0] == "#"]
    
    processed_tweet = tweet
    for hashtag in hashtags:
        processed_tweet = processed_tweet.replace(hashtag, hashtag[1:])
        
    return processed_tweet
    
def split_sentences(tweet):
    possible_sentence_boundaries = find_possible_sentence_boundaries(tweet)
    sentence_boundaries = find_sentence_boundaries(tweet, possible_sentence_boundaries)
    processed_tweet = tweet
    for bound in reversed(sentence_boundaries):
	    processed_tweet = insert(processed_tweet, "\n", bound + 1)
    return processed_tweet
        
def find_possible_sentence_boundaries(tweet):
    possible_sentence_boundaries = []
    tweet_characters = list(tweet)
    for i in range(0, len(tweet_characters)):
        if (tweet_characters[i] in set([".", "?", "!"])):
            possible_sentence_boundaries.append(i)
    return possible_sentence_boundaries
    
def find_sentence_boundaries(tweet, possible_sentence_boundaries):
    real_sentence_boundaries = possible_sentence_boundaries
    discarded_sentence_boundaries = []
    for index, sentence_boundary in enumerate(possible_sentence_boundaries):
       if (sentence_boundary >= len(tweet)-1):
           continue
       if (tweet[sentence_boundary+1] == "\""):
           real_sentence_boundaries[index] += 1
           continue
       if (tweet[sentence_boundary] in set([".", "?", "!"]) and not is_boundary(sentence_boundary, tweet)):
           discarded_sentence_boundaries.append(sentence_boundary)
    return diff(possible_sentence_boundaries, discarded_sentence_boundaries)

def is_boundary(sentence_boundary, tweet):
    if (sentence_boundary+1 < len(tweet) and tweet[sentence_boundary+1] in set([".", "?", "!"])):
        return False
    
    abbreviation = ""
    for i in range(sentence_boundary, 0, -1):
      if tweet[i] == " ":
          break
      abbreviation = tweet[i] + abbreviation
    
    if (tweet[sentence_boundary] == "." and re.match(PROP_ABBREV_REGEX, abbreviation)):
        return False
    if (tweet[sentence_boundary] == "." and sentence_boundary+3 < len(tweet) and re.match(INLINE_ABBREV_REGEX, abbreviation)):
        if(tweet[sentence_boundary + 1] != " " and tweet[sentence_boundary + 1].islower()):
            return False
        if(tweet[sentence_boundary + 2] != " " and tweet[sentence_boundary + 2].islower()):
            return False
    return True
    
def insert(original, new, pos):
	if (pos == len(original)-1):
		return original + new
	return original[:pos] + new + original[pos:]
	
def diff(first, second):
    second = set(second)
    return [item for item in first if item not in second]

def split_clitics(tweet):
    return re.sub(CLITICS_REGEX, r' \1', tweet)
    
def tag(tweet, tagger):
    tokens = list(filter(lambda x: x != '', tweet.split(" ")))
    tags = tagger.tag(tokens)
    processed_tweet = ' '.join('%s/%s' % t for t in zip(tokens, tags))
    return re.sub(r'([.?!])\n/([A-Z][A-Z])', r'\1/\2\n', processed_tweet)

if __name__ == "__main__":
    tagger = NLPlib.NLPlib()
    f = open(sys.argv[3], 'w')

    with open(sys.argv[1], 'rb') as twitter_csv:
        reader = csv.reader(twitter_csv)
        for row in reader:
            f.write("<A=%s>\n" % row[0])
            f.write(tag(process(row[5]), tagger))
    
