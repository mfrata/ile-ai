from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

from ile.schemas import AllTxnInfo, TxnInfo

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

model = OpenAIModel("gpt-4o")

extractor_agent = Agent(
    model,
    output_type=AllTxnInfo,
    system_prompt=SYSTEM,
)


def extract_transactions(transactions_text: str) -> list[TxnInfo]:
    result: AllTxnInfo = extractor_agent.run_sync(USER.format(transactions_text=transactions_text)).output
    return result.all_txn
