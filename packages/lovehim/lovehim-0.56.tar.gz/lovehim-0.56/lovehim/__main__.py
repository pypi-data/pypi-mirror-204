"""

import argparse
import openai
from .get_verse import generate_verse

# Set up the OpenAI API key
openai.api_key = "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"

# Parse the command-line arguments
parser = argparse.ArgumentParser(description='Get a Bible verse based on a topic')
parser.add_argument('topic', nargs='+', help='the topic you want the verse to be about')
args = parser.parse_args()

# Call the generate_verse function with the user-specified topic
topic = ' '.join(args.topic)
verse = generate_verse(topic)

# Print out the resulting Bible verse
print(verse)
"""

from .get_verse import main

# Call the main function with the user-specified topic
verse = main()

# Print out the resulting Bible verse
print(verse)
