from __future__ import annotations

import json
from enum import StrEnum, auto

from pydantic import BaseModel, Field


class FinancialInstitution(StrEnum):
    """
    Different financial institution categories.
    """
    N26: str = auto()
    XP: str = auto()
    NUBANK: str = auto()
    C6: str = auto()
    AMEX: str = auto()
    MILESANDMORE: str = auto()



class Currency(StrEnum):
    """
    Different currency categories.
    """
    EUR: str = auto()
    USD: str = auto()
    BRL: str = auto()

    @classmethod
    def get_main_currency(cls) -> Currency:
        return Currency.EUR
    
    @classmethod
    def get_currency_from_financial_institution(cls, financial_institution: FinancialInstitution) -> Currency:
        match financial_institution:
            case FinancialInstitution.N26:
                return Currency.EUR
            case FinancialInstitution.XP:
                return Currency.BRL
            case FinancialInstitution.NUBANK:
                return Currency.BRL
            case FinancialInstitution.C6:
                return Currency.BRL
            case FinancialInstitution.AMEX:
                return Currency.EUR
            case FinancialInstitution.MILESANDMORE:
                return Currency.EUR
            case _:
                return Currency.get_main_currency()


class Budgets(StrEnum):
    """
    Different budget categories.

    Attributes:
        n26: Represents the N26 budget category, typically associated with salary and income-related transactions.
        bolsinha: Serves for categories like rent, groceries, expenses like cellphone, gym, and delivery.
        general: Represents the general budget category.
    """
    n26: str = auto()
    bolsinha: str = auto()
    general: str = auto()


class Categories(StrEnum):
    """
    Different budget categories.

    Attributes:
        commute: Represents expenses related to commuting, such as public transport or fuel.
        delivery: Covers expenses for delivery services.
        education: Includes expenses related to educational purposes.
        groceries: Represents spending on groceries.
        health: Covers health-related expenses.
        income: Represents income transactions.
        out_meals: Covers expenses for meals eaten out.
        payments: Represents various payment transactions.
        rent: Covers rent-related expenses.
        giving: Represents donations or gifts.
        selftransfer: Represents transfers between personal accounts.
        services: Covers expenses for various services.
        transfer: Represents money transfers.
        travel: Covers travel-related expenses.
        investing: Represents investment-related transactions.
    """
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
    financial_institution: FinancialInstitution = Field(
        default=FinancialInstitution.N26, 
        description="The financial institution of the transaction",
    )
    date: str = Field(
        ...,
        description="The date of the transaction, format DD/MM/YYYY",
    )
    date_month: str = Field(
        ...,
        description="The last day of the month of the transaction in the format DD/MM/YYYY",
    )
    description: str = Field(
        ...,
        description="A brief description of the transaction, with phrases, names or codes info of the transaction"
    )
    value: float = Field(..., description="The monetary value of the transaction")
    currency: Currency = Field(
        default=Currency.get_currency_from_financial_institution(financial_institution), 
        description="The currency of the transaction"
    )
    budget: Budgets = Field( ..., description=f"{Budgets.__doc__}",)
    category: Categories = Field(..., description=f"{Categories.__doc__}",)
    tags: str = Field(default_factory=str, description="To be added by the user, do not populate")


class AllTxnInfo(BaseModel):
    all_txn: list[TxnInfo]

    @classmethod
    def from_str(cls, string: str) -> AllTxnInfo:
        return cls(**json.loads(string))
