from typing import Literal

from pydantic_ai import Agent, BinaryContent

from ile.schemas import AllTxnInfo, TxnInfo

SYSTEM = "You are a extractor of transactions from a file"
USER = """
Return the list of transactions from this text

# INSTRUCTIONS
* all text that looks like a phrase, names or code should be include in the descriptions
"2023-11-10","blablabla","LU897510","Income","papapa","0.01","","",""
description = blablabla LU897510 papapa

Also identify the financial institution for all transactions of this file
use the file name as well: {file_name}

"2023-11-10","Alice","DE897510","Income","burgerkiller","0.01","","",""
description = Alice DE897510 burgerkiller

# TRANSACTIONS
"""

extractor_agent = Agent(
    model="google-gla:gemini-2.0-flash",
    output_type=AllTxnInfo,
    system_prompt=SYSTEM,
)


async def extract_transactions(
    file: bytes,
    file_name: str,
    media_type: Literal["application/pdf", "text/csv"] = "application/pdf",
) -> list[TxnInfo]:
    result = await extractor_agent.run([
        USER.format(file_name=file_name),
        BinaryContent(data=file, media_type=media_type),
    ])
    agent_output: AllTxnInfo = result.output
    return agent_output.all_txn
