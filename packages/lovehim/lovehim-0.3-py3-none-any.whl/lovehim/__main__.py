import argparse
import openai
from .get_verse import generate_verse

# Set up the OpenAI API key
openai.api_key = "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"

# Parse the command-line arguments
parser = argparse.ArgumentParser(description='Get a Bible verse based on a topic')
parser.add_argument('topic', type=str, help='the topic you want the verse to be about')
args = parser.parse_args()

# Call the generate_verse function with the user-specified topic
verse = generate_verse(args.topic)

# Print out the resulting Bible verse
print(verse)
