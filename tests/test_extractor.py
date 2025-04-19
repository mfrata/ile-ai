import pytest
import pytest_asyncio


from ile.extractor import extract_transactions
from ile.schemas import Budgets, Categories


SAMPLE_CSV = """"
Date","Payee","Account number","Transaction type","Payment reference","Amount (EUR)","Amount (Foreign Currency)","Type Foreign Currency","Exchange Rate"
"2023-11-08","From Root to Main Account","","Income","From Savings to Main Account","500.0","","",""
"2023-11-10","PayPal Europe S.a.r.l. et Cie S.C.A","LU897510","Income","PP.9081.PP/YYR1030524472934","0.01","","",""
"2023-11-13","Alice","DE731001100","MoneyBeam","Split the bill request for Burgerkiller","-23.9","","",""
"2023-11-13","Alice","DE731001100","MoneyBeam","Split the bill request for climbing Block","-12.0","","",""
"2023-11-13","Alice","DE73100110","MoneyBeam","uau hoa 12/11/2023","-18.4","","",""
"""

@pytest_asyncio.fixture(scope="module")
async def extracted_transactions():
    return await extract_transactions(SAMPLE_CSV)

test_cases = [
    (
        0,
        "2023-11-08",
        "500.0",
        ["From Savings to Main Account"]
    ),
    (
        1,
        "2023-11-10",
        "0.01",
        ["PayPal Europe S.a.r.l. et Cie", "LU897510", "PP.9081.PP/YYR1030524472934"]
    ),
    (
        2,
        "2023-11-13",
        "-23.9",
        ["Alice", "DE731001100", "Burgerkiller"]
    ),
    (
        3,
        "2023-11-13",
        "-12.0",
        ["Alice", "DE731001100", "climbing Block"]
    ),
    (
        4,
        "2023-11-13",
        "-18.4",
        ["Alice", "DE73100110", "uau hoa 12/11/2023"]
    ),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("index, expected_date, expected_value, expected_phrases", test_cases)
async def test_transaction_fields(index, expected_date, expected_value, expected_phrases, extracted_transactions):
    txn = extracted_transactions[index]

    assert txn.date == expected_date
    assert txn.date_month == expected_date[:7]
    assert txn.value == expected_value
    assert Budgets(txn.budget)
    assert Categories(txn.category)

    for phrase in expected_phrases:
        assert phrase in txn.description

