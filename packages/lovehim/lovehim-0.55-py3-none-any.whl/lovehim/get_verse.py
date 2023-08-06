import openai
import argparse

# Set up the OpenAI API key
openai.api_key = "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"

# Define the function to generate a Bible verse based on a topic
def generate_verse(topic):
    prompt = f"Generate a Bible verse about {topic}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5,
        presence_penalty=0.5,
    )
    verse = response.choices[0].text.strip()
    return verse

def main():
    parser = argparse.ArgumentParser(description='Get a Bible verse based on a topic')
    parser.add_argument('topic', nargs='+', help='the topic you want the verse to be about')
    args = parser.parse_args()
    topic = ' '.join(args.topic)
    verse = generate_verse(topic)
    print(verse)

if __name__ == '__main__':
    main()