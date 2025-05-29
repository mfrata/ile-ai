import streamlit as st
import pandas as pd
import asyncio
from ile.extractor import extract_transactions
from ile.schemas import Budgets, Categories


def initialize_session_state():
    """Initialize session state variables."""
    if "transactions" not in st.session_state:
        st.session_state.transactions = []
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "is_processing" not in st.session_state:
        st.session_state.is_processing = False
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = set()
    if "current_edits" not in st.session_state:
        st.session_state.current_edits = {}
    if "pending_files" not in st.session_state:
        st.session_state.pending_files = []
    if "navigation_triggered" not in st.session_state:
        st.session_state.navigation_triggered = False


def save_transaction_changes(transaction, date, value, description, budget, category, tags):
    """Save changes to the transaction."""
    transaction.date = date.strftime("%Y-%m-%d")
    transaction.date_month = date.strftime("%Y-%m")
    transaction.value = value
    transaction.description = description
    transaction.budget = budget
    transaction.category = category
    transaction.tags = tags


def display_transaction_editor(transaction):
    """Display the transaction editing interface."""
    st.subheader("Edit Transaction Details")
    
    # Create two columns for the form
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
    
    # Add tags field below the columns
    tags = st.text_input("Tags", value=transaction.tags, help="Add tags separated by commas")
    
    return date, value, description, budget, category, tags


async def process_file(uploaded_file):
    """Process uploaded file and return transactions."""
    content = uploaded_file.getvalue()
    media_type = "application/pdf" if uploaded_file.name.endswith(".pdf") else "text/csv"
    return await extract_transactions(content, media_type)


def start_ui():
    """Main UI function."""
    st.title("Transaction Extractor & Editor")
    initialize_session_state()

    # File uploader
    uploaded_files = st.file_uploader(
        "Upload your transaction files",
        type=["csv", "pdf"],
        help="Upload CSV or PDF files containing transaction data",
        accept_multiple_files=True
    )

    # Add new files to pending list
    if uploaded_files:
        for file in uploaded_files:
            if file.name not in st.session_state.processed_files and file not in st.session_state.pending_files:
                st.session_state.pending_files.append(file)

    # Process pending files one at a time
    if st.session_state.pending_files:
        current_file = st.session_state.pending_files[0]
        try:
            with st.spinner(f"Extracting transactions from {current_file.name}..."):
                # Store current edits before adding new transactions
                if st.session_state.transactions:
                    current_txn = st.session_state.transactions[st.session_state.current_index]
                    st.session_state.current_edits = {
                        'date': pd.to_datetime(current_txn.date),
                        'value': current_txn.value,
                        'description': current_txn.description,
                        'budget': current_txn.budget,
                        'category': current_txn.category,
                        'tags': current_txn.tags
                    }

                # Process file
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    new_transactions = loop.run_until_complete(process_file(current_file))
                    st.session_state.transactions.extend(new_transactions)
                    st.session_state.processed_files.add(current_file.name)
                    st.success(f"Successfully extracted {len(new_transactions)} transactions from {current_file.name}!")
                finally:
                    loop.close()

                # Remove processed file from pending list
                st.session_state.pending_files.pop(0)
                st.rerun()

        except Exception as e:
            st.error(f"Error processing {current_file.name}: {str(e)}")
            st.info("Please make sure your file is in the correct format and try again.")
            # Remove failed file from pending list
            st.session_state.pending_files.pop(0)
            st.rerun()

    # Display navigation and editor only if we have transactions
    if st.session_state.transactions:
        st.write(f"Total transactions: {len(st.session_state.transactions)}")
        
        # Get current transaction
        current_txn = st.session_state.transactions[st.session_state.current_index]
        
        # Display editor and get values
        date, value, description, budget, category, tags = display_transaction_editor(current_txn)

        # Navigation controls
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.button("⬅️ Previous") and st.session_state.current_index > 0:
                # Save current changes before moving
                save_transaction_changes(current_txn, date, value, description, budget, category, tags)
                st.session_state.current_index -= 1
                st.session_state.navigation_triggered = True
                st.rerun()
        with col2:
            st.write(f"Transaction {st.session_state.current_index + 1} of {len(st.session_state.transactions)}")
        with col3:
            if st.button("Next ➡️") and st.session_state.current_index < len(st.session_state.transactions) - 1:
                # Save current changes before moving
                save_transaction_changes(current_txn, date, value, description, budget, category, tags)
                st.session_state.current_index += 1
                st.session_state.navigation_triggered = True
                st.rerun()

        # Display raw transaction data in an expander
        with st.expander("View Raw Transaction Data"):
            st.json(current_txn.model_dump())

        # Reset navigation trigger after displaying everything
        st.session_state.navigation_triggered = False




