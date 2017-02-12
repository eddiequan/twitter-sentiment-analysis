import sys
import re

SLANG = ["smh",  "fwb",  "lmfao",  "lmao",  "lms",  "tbh",  "rofl",  "wtf",  "bff",  "wyd",  "lylc",  "brb",  "atm",  "imao",  "sml",  "btw",
"bw",  "imho",  "fyi",  "ppl",  "sob",  "ttyl",  "imo",  "ltr",  "thx",  "kk",  "omg",  "ttys",  "afn",  "bbs",  "cya",  "ez",  "f2f",  "gtr",
"ic", "jk", "k", "ly", "ya", "nm", "np", "plz", "ru", "so", "tc", "tmi", "ym", "ur", "u", "sol", "lol", "imo", "tbh", "fam", "fml"]

SLANG_REGEX = "(" + "|".join(SLANG) + ")"

def split_by_demarcation(data):
    return re.split(r'(<A=[0|4]>)', data)[1:]

# First person pronouns
def feat1(content):
    return len(re.findall(r'\b(i/PRP|me/|my/|mine/|we/|us/|our/|ours/)', content, re.IGNORECASE))

# Second person pronouns
def feat2(content):
    # print("feat2 finds")
    # print(re.findall(', content, re.IGNORECASE))

    return len(re.findall(r'\b(you/|your/|yours/|u/|ur/|urs/)', content, re.IGNORECASE))

# Third person pronouns
def feat3(content):
    # print("feat3 finds")
    # print(re.findall(r'\b(he/|him/|his/|she/|her/|hers/|it/|its/|they/|them/|their/|theirs/)', content, re.IGNORECASE))

    return len(re.findall(r'\b(he/|him/|his/|she/|her/|hers/|it/|its/|they/|them/|their/|theirs/)', content, re.IGNORECASE))

# Coordinating Conjuctions
def feat4(content):
    # print("feat4 finds")
    # print(re.findall(r'/CC', content))
    return len(re.findall(r'/CC', content))

# Past tense verbs
def feat5(content):
    return len(re.findall(r'/VBD|/VBN', content))

# Future tense verbs
def feat6(content):
    # print("feat6 finds")

    # print(re.findall(r'(going/[A-Z]+ to/[A-Z]+ \w+/VB\b)|((\'ll/[A-Z]+|will/[A-Z]+|gonna/[A-Z]+) \w+/VB\b)', content, re.IGNORECASE))
    return len(re.findall(r'(going/[A-Z]+ to/[A-Z]+ \w+/VB\b)|((\'ll/[A-Z]+|will/[A-Z]+|gonna/[A-Z]+) \w+/VB\b)', content, re.IGNORECASE))

# Commas
def feat7(content):
    return len(re.findall(r',/,', content))


# Semicolons / Colons
def feat8(content):
    return len(re.findall(r':/:|;/:', content))
    
# Dashes
def feat9(content):
    return len(re.findall(r'-/:', content))

# Parens
def feat10(content):
    return len(re.findall(r'\(/\(|\)/\)', content))

# Ellipses
def feat11(content):
    return len(re.findall(r'(\.\.+)', content))

# Common Nouns
def feat12(content):
    return len(re.findall(r'/(NN\b|NNS\b)', content))

# Proper Nouns
def feat13(content):
    return len(re.findall(r'/(NNP\b|NNPS\b)', content))

# Adverbs
def feat14(content):
    return len(re.findall(r'/(RB\b|RBR\b|RBS\b)', content))

# wh words
def feat15(content):
    return len(re.findall(r'/(WDT\b|WP\b|WP\$\b|WRB\b)', content))

# slang lul
def feat16(content):
    return len(re.findall(SLANG_REGEX, content))

# CAPS WORDS
def feat17(content):
    return len(re.findall(r'[A-Z][A-Z]+/', content))

# avg. num. words per sentence
def feat18(content):
    sentences = content.lstrip().rstrip().split("\n")
    num_tokens = 0
    for sentence in sentences:
        num_tokens += len(sentence.lstrip().rstrip().split(" "))

    return num_tokens / len(sentences)

# avg. length of words
def feat19(content):
    non_punctuation_tokens = re.findall(r'(\w+\W?)/[A-Z]+\b', content)
    if (len(non_punctuation_tokens) == 0):
        return 0
    num_chars = 0
    for token in non_punctuation_tokens:
        num_chars += len(token)

    return num_chars / len(non_punctuation_tokens)


# num sentences
def feat20(content):
    # We want to remove the newlines from the beginning of the content
    sentences = content.lstrip().rstrip().split("\n")
    return len(sentences)

def format_features(content):
    features = [
        feat1(content),
        feat2(content),
        feat3(content),
        feat4(content),
        feat5(content),
        feat6(content),
        feat7(content),
        feat8(content),
        feat9(content),
        feat10(content),
        feat11(content),
        feat12(content),
        feat13(content),
        feat14(content),
        feat15(content),
        feat16(content),
        feat17(content),
        feat18(content),
        feat19(content),
        feat20(content),

    ]
    return ",".join(str(x) for x in features)

def format_affect(tag):
    return re.search(r'<A=(\d)>', tag).group(1)

def initialize_data_points(classes):
    d = {}
    for class_id in classes:
        d[class_id] = 0
    return d


if __name__ == "__main__":
    output_file = open(sys.argv[2], 'w')

    with open(sys.argv[1], 'rb') as input_data:
        data = input_data.read()

    parsed_file_array = split_by_demarcation(data)
    polarity_tags = list(format_affect(x) for x in parsed_file_array[::2])
    tagged_tweet_content = parsed_file_array[1::2]

    if (len(sys.argv) > 3):
        MAX_PER_CLASS = int(sys.argv[3])
        classes = list(set(polarity_tags))
        num_data_points = initialize_data_points(classes)

        for idx, content in enumerate(tagged_tweet_content):
            if not (num_data_points[polarity_tags[idx]] >= MAX_PER_CLASS):
                output_file.write(format_features(content) + "," + polarity_tags[idx] + "\n")
                num_data_points[polarity_tags[idx]] += 1
    else:
        for idx, content in enumerate(tagged_tweet_content):
            output_file.write(format_features(content) + "," + polarity_tags[idx] + "\n")

    output_file.close()



