from openai import OpenAI

from ile.schemas import AllTxnInfo, TxnInfo

client = OpenAI()

SYSTEM = "You are a extractor of transactions from a file"
USER = """
Return the list of transactions from this text

# INSTRUCTIONS
* all text that looks like a phrase, names or code should be include in the descriptions
"2023-11-10","blablabla","LU897510","Income","papapa","0.01","","",""
description = blablabla LU897510 papapa

"2023-11-10","Alice","DE897510","Income","burgerkiller","0.01","","",""
description = Alice DE897510 burgerkiller

# TRANSACTIONS
{transactions_text},
"""


def extract_transactions(transactions_text: str) -> list[TxnInfo]:
    response = client.beta.chat.completions.parse(
        model="gpt-4.1-nano",
        messages=[
            {
                "role": "system",
                "content": SYSTEM,
            },
            {
                "role": "user",
                "content": USER.format(transactions_text=transactions_text),
            },
        ],
        response_format=AllTxnInfo,
        temperature=0
    )

    parsed = AllTxnInfo.from_str(response.choices[0].message.content)
    return parsed.all_txn
