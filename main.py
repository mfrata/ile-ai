from enum import StrEnum, auto
import sys
from datetime import datetime
from openai import OpenAI
from pydantic import BaseModel, Field


class Budgets(StrEnum):
    n26: str = auto()
    bolsinha: str = auto()
    general: str = auto()


class Categories(StrEnum):
    commute: str = auto()
    delivery: str = auto()
    education: str = auto()
    groceries: str = auto()
    health: str = auto()
    income: str = auto()
    out_meals: str = auto()
    payments: str = auto()
    rent: str = auto()
    giving: str = auto()
    selftransfer: str = auto()
    services: str = auto()
    transfer: str = auto()
    travel: str = auto()
    investing: str = auto()


class TxnInfo(BaseModel):
    date: str = Field(..., description="The date of the transaction")
    date_month: str = Field(..., description="The month of the transaction")
    description: str = Field(..., description="A brief description of the transaction")
    value: str = Field(..., description="The monetary value of the transaction")
    budget: Budgets = Field(..., description="The budget category for the transaction")
    category: Categories = Field(..., description="The category of the transaction")
    tags: str = Field(default_factory=str, description="To be added by the user, do not populate")


class AllTxnInfo(BaseModel):
    all_txn: list[TxnInfo]


client = OpenAI()


transactions_text = open(sys.argv[1]).read()

response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a extractor of transactions from a file"},
        {"role": "user", "content": f"Return the list of transactions from this text: \n {transactions_text}"},
    ],
    response_format=AllTxnInfo,
)

print(response.choices[0].message.content)
