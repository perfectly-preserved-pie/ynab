from dotenv import load_dotenv
from typing import List, Dict, Any
import os
import requests
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Get the access token and budget ID from environment variables
access_token = os.environ.get("YNAB_ACCESS_TOKEN")
budget_id = os.environ.get("YNAB_BUDGET_ID")

def get_ynab_transactions(
    access_token: str, budget_id: str, memo_filter: str
) -> pd.DataFrame:
    """
    Fetches a list of transactions from the YNAB API for a specified budget and filters them by memo.
    Returns a pandas DataFrame containing 'date', 'category_name', and 'memo' for each filtered transaction.

    :param access_token: Your YNAB personal access token
    :param budget_id: The YNAB budget ID from which to retrieve transactions
    :param memo_filter: A substring to search for in each transaction's memo field (case insensitive)
    :return: A pandas DataFrame containing 'date', 'category_name', and 'memo' columns.
    """
    # Endpoint format for transactions in a specific budget
    url = f"https://api.youneedabudget.com/v1/budgets/{budget_id}/transactions"
    
    # Set up the headers with your access token
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    # Make the request to the YNAB API
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response JSON and retrieve all transactions
        transactions = response.json()['data']['transactions']
        
        # Filter the transactions
        filtered_transactions = [
            {
                'date': transaction['date'],
                'category_name': transaction['category_name'],
                'memo': transaction['memo']
            }
            for transaction in transactions
            if transaction['memo'] and memo_filter.lower() in transaction['memo'].lower()
        ]
        
        # Create DataFrame
        df = pd.DataFrame(filtered_transactions, columns=['date', 'category_name', 'memo'])
        return df
    else:
        # Handle possible errors
        response.raise_for_status()

# Prompt for memo filter
memo_filter = input("Enter a memo filter: ")

try:
    df_transactions = get_ynab_transactions(access_token, budget_id, memo_filter)
    print(df_transactions)
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
