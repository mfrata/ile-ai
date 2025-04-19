import sys
from openai import OpenAI

client = OpenAI()

transactions_text = open(sys.argv[1]).read()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a extractor of transactions from a file"},
        {"role": "user", "content": f"Return the list of transactions from this text: \n {transactions_text}"},
    ],
)

print(response.choices[0].message.content)
