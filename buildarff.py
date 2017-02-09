import sys
import re

def split_by_demarcation(data):
    return re.split(r'(<A=[0|4]>)', data)[1:]

# First person pronouns
def feat1(content):
    return len(re.findall(r'\b(i/PRP|me/|my/|mine/|we/|us/|our/|ours/)', content, re.IGNORECASE))

# Second person pronouns
def feat2(content):
    print("feat2 finds")
    print(re.findall(r'\b(you/|your/|yours/|u/|ur/|urs/)', content, re.IGNORECASE))

    return len(re.findall(r'\b(me/|my/|mine/|we/|us/|our/|ours/)', content, re.IGNORECASE))

# Third person pronouns
def feat3(content):
    print("feat3 finds")
    print(re.findall(r'\b(he/|him/|his/|she/|her/|hers/|it/|its/|they/|them/|their/|theirs/)', content, re.IGNORECASE))

    return len(re.findall(r'\b(he/|him/|his/|she/|her/|hers/|it/|its/|they/|them/|their/|theirs/)', content, re.IGNORECASE))

# Coordinating Conjuctions
def feat4(content):
    print("feat4 finds")
    print(re.findall(r'/CC', content))
    return len(re.findall(r'/CC', content))

# Past tense verbs
def feat5(content):
    print("feat5 finds")
    print(re.findall(r'/VBD', content))
    return len(re.findall(r'/VBD', content))

# Future tense verbs
def feat6(content):
    print("feat6 finds")

    print(re.findall(r'(going/[A-Z]+ to/[A-Z]+ \w+/VB\b)|((\'ll/[A-Z]+|will/[A-Z]+|gonna/[A-Z]+) \w+/VB\b)', content))
    return len(re.findall(r'(going/[A-Z]+ to/[A-Z]+ \w+/VB\b)|((\'ll/[A-Z]+|will/[A-Z]+|gonna/[A-Z]+) \w+/VB\b)', content))

# Commas
def feat7(content):
    print("feat7 finds")

    print(re.findall(r',/,', content))
    return len(re.findall(r',/,', content))


# Semicolons / Colons
def feat8(content):
    print("feat8 finds")
    print(re.findall(r':/:|;/;', content))
    return len(re.findall(r':/:|;/;', content))
    

# Dashes
def feat9(content):
    print("feat9 finds")

    print(re.findall(r'-/-', content))
    return len(re.findall(r'-/-', content))

if __name__ == "__main__":
    output_file = open(sys.argv[2], 'w')

    with open(sys.argv[1], 'rb') as input_data:
        data = input_data.read()

    parsed_file_array = split_by_demarcation(data)
    polarity_tags = parsed_file_array[::2]
    tagged_tweet_content = parsed_file_array[1::2]
    for idx, content in enumerate(tagged_tweet_content):
        print("===========================================")
        print(feat1(content))
        print(feat2(content))
        print(feat3(content))
        print(feat4(content))

        print("===========================================")

    print(polarity_tags)
    print(tagged_tweet_content)

