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


def test_extract_transactions():
    transactions = extract_transactions(SAMPLE_CSV)

    assert len(transactions) == 5  # noqa[PLR2004]

    # Test first transaction (Supermarket)
    txn = transactions[0]
    assert txn.date == "2023-11-08"
    assert txn.date_month == "2023-11"
    assert txn.value == "500.0"
    assert Budgets(txn.budget)
    assert Categories(txn.category)

    txn = transactions[1]
    assert txn.date == "2023-11-10"
    assert txn.date_month == "2023-11"
    assert txn.value == "0.01"
    assert Budgets(txn.budget)
    assert Categories(txn.category)

    txn = transactions[2]
    assert txn.date == "2023-11-13"
    assert txn.date_month == "2023-11"
    assert txn.value == "-23.9"
    assert Budgets(txn.budget)
    assert Categories(txn.category)

    txn = transactions[3]
    assert txn.date == "2023-11-13"
    assert txn.date_month == "2023-11"
    assert txn.value == "-12.0"
    assert Budgets(txn.budget)
    assert Categories(txn.category)

    txn = transactions[-1]
    assert txn.date == "2023-11-13"
    assert txn.date_month == "2023-11"
    assert txn.value == "-18.4"
    assert Budgets(txn.budget)
    assert Categories(txn.category)
