import streamlit as st
import pandas as pd

from ile.extractor import extract_transactions
from ile.schemas import Budgets, Categories


def initialize_session_state():
    if "transactions" not in st.session_state:
        st.session_state.transactions = []
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0


def display_transaction_editor(transaction):
    st.subheader("Edit Transaction Details")

    # Create columns for the form
    col1, col2 = st.columns(2)

    with col1:
        date = st.date_input("Date", value=pd.to_datetime(transaction.date))
        value = st.text_input("Amount", value=transaction.value)
        budget = st.selectbox(
            "Budget",
            options=[b.value for b in Budgets],
            index=[b.value for b in Budgets].index(transaction.budget)
        )

    with col2:
        description = st.text_area("Description", value=transaction.description, height=100)
        category = st.selectbox(
            "Category",
            options=[c.value for c in Categories],
            index=[c.value for c in Categories].index(transaction.category)
        )

    # Save button
    if st.button("Save Changes"):
        transaction.date = date.strftime("%Y-%m-%d")
        transaction.date_month = date.strftime("%Y-%m")
        transaction.value = value
        transaction.description = description
        transaction.budget = budget
        transaction.category = category
        st.success("Changes saved!")


async def process_file(uploaded_file):
    """Process uploaded file and return transactions."""
    content = uploaded_file.getvalue()
    return await extract_transactions(content)


async def start_ui():
    st.title("Transaction Editor")
    initialize_session_state()

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload file",
        type=["csv", "pdf"],
        help="Upload a CSV or PDF file containing transaction data"
    )

    if uploaded_file is not None:
        try:
            # Process the file and extract transactions
            transactions = await process_file(uploaded_file)
            st.session_state.transactions = transactions

            # Display transaction count
            st.write(f"Found {len(transactions)} transactions")

            # Navigation controls
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                if st.button("Previous") and st.session_state.current_index > 0:
                    st.session_state.current_index -= 1
            with col2:
                st.write(f"Transaction {st.session_state.current_index + 1} of {len(transactions)}")
            with col3:
                if st.button("Next") and st.session_state.current_index < len(transactions) - 1:
                    st.session_state.current_index += 1

            # Display current transaction
            if st.session_state.transactions:
                current_txn = st.session_state.transactions[st.session_state.current_index]
                display_transaction_editor(current_txn)

                # Display raw transaction data
                with st.expander("Raw Transaction Data"):
                    st.json(current_txn.model_dump())
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
