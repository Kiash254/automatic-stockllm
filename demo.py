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
AT_API = "f69b3b08e0f685a438205869737527f30151bb18e22dd12ef73ee12b9e8852fe"
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
st.set_page_config(page_title="Supermarket Stock Information")
st.header("Supermarket Stock Information")

# User input for the question
question = st.text_input("Enter your question", key='input')

# Button to submit the question
submit = st.button("Ask Question")

if submit:
    # Get the SQL query from the English question
    response = get_gemini_response(question, prompt)
    # Retrieve the data from the database using the SQL query
    rows = read_sql_query(response, "supermarket.db")
    # Display the response
    st.subheader("Response:")
    for row in rows:
        st.write(row)
