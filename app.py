# Import necessary libraries
import streamlit as st
from dotenv import load_dotenv
import os
import sqlite3
import africastalking
import google.generativeai as genai

# Load the environment variables
load_dotenv()

# Configure the API key for Gen AI
genai.configure(api_key=os.getenv("Google_api_key"))

# Configure the API key and username for Africastalking
AT_API = "0fd2f09f57ba6a4b55cc7551918ac6f324658988500c39ee4f5e7be619671a82"
AT_USERNAME = "stockllm"

# Initialize Africastalking
africastalking.initialize(AT_USERNAME, AT_API)
sms = africastalking.SMS

# Create a function to load the Gen AI model and provide the SQL query
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    full_prompt = prompt[0] + " " + question
    response = model.generate_content(full_prompt)
    # Remove Markdown syntax from the SQL query
    sql_query = response.text.replace("```sql", "").replace("```", "")
    return sql_query



# Function to retrieve data from the database using the SQL query
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()

    conn.close()
    return rows

# Define the Prompt
prompt = [
    """
    You are an expert in converting English questions into SQL code!
    The SQL database has the name PRODUCTS and has the following columns - NAME, CATEGORY, PRICE, QUANTITY\n\n
    For example,\nExample 1 - How many products are in stock?,
    the SQL command will be something like this SELECT COUNT(*) FROM PRODUCTS ;
    
    \nExample 2 - Tell me the stock of a specific product?,
    the SQL command will be something like this SELECT QUANTITY FROM PRODUCTS WHERE NAME = 'product_name' ;
    where 'product_name' is the name of the product you want to check the stock for.
    """
]

# Setting up the Streamlit app
st.set_page_config(page_title=" Mini Supermarket    Stock Retriver")
st.header("Mini Supermarket    Stock Retriver")

# User input for the question
question = st.text_input("Enter your question", key='input')

# User input for the manager's name
manager_name = st.text_input("Enter manager's name")

# User input for the manager's phone number
manager_phone_number = st.text_input("Enter manager's phone number")

# Button to submit the question
submit = st.button("Ask Question")

if submit:
    # Get the SQL query from the English question
    response = get_gemini_response(question, prompt)
    # Retrieve the data from the database using the SQL query
    rows = read_sql_query(response, "supermarket.db")
    # Get the total number of items in the database
    total_items = len(rows)
    # Calculate the stock status based on the total number of items
    stock_status = "Increase stock" if total_items < 100 else "Stock is sufficient"
    
    # Display the response
    st.subheader("Response:")
    for row in rows:
        st.write(row)
        
    
  
    # print(type(row))
    # Send SMS to the manager
    message = f"Dear {manager_name}, your stock status has been updated. {stock_status}. Total items in database: {total_items}. Please check your inventory.\n\nResponse: {rows}"
    sms_response = sms.send(message, [manager_phone_number])
    
    st.write(f"SMS sent to {manager_name} at {manager_phone_number}")

