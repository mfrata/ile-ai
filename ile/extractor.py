from openai import OpenAI

from ile.schemas import AllTxnInfo

client = OpenAI()


def extract_transactions(transactions_text: str) -> str:
    response = client.beta.chat.completions.parse(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a extractor of transactions from a file",
            },
            {
                "role": "user",
                "content": f"Return the list of transactions from this text: \n {transactions_text}",
            },
        ],
        response_format=AllTxnInfo,
    )

    return response.choices[0].message.content
