import streamlit as st
from dotenv import load_dotenv
import os
import sqlite3
import africastalking
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the environment variables
load_dotenv()

# Configure the API key for Gen AI
genai.configure(api_key=os.getenv("Google_api_key"))

# Configure the API key and username for Africastalking
AT_API=os.getenv("AT_API")
AT_USERNAME=os.getenv("AT_USERNAME")

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
st.set_page_config(page_title=" Mini Supermarket    Stock Retriver Using AI")
st.header("Mini Supermarket    Stock Retriver Using AI")

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
    # Convert rows to DataFrame for visualization
    df = pd.DataFrame(rows, columns=['NAME', 'CATEGORY', 'PRICE', 'QUANTITY'])
    
    # Visualization part
    col1, col2 = st.columns(2)

    columns = df.columns.tolist()

    with col1:
        st.write("")
        st.write(df.head())

    with col2:
        # Allow the user to select columns for plotting
        selected_columns = st.multiselect('Select the columns to visualize', options=columns)

        plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
        # Allow the user to select the type of plot
        plot_type = st.selectbox('Select the type of plot', options=plot_list)

    # Generate the plot based on user selection
    if st.button('Generate Plot') and selected_columns:

        fig, ax = plt.subplots(figsize=(6, 4))

        if plot_type == 'Line Plot':
            df[selected_columns].plot(kind='line', ax=ax)
        elif plot_type == 'Bar Chart':
            df[selected_columns].plot(kind='bar', ax=ax)
        elif plot_type == 'Scatter Plot':
            df[selected_columns].plot(kind='scatter', x=selected_columns[0], y=selected_columns[1], ax=ax)
        elif plot_type == 'Distribution Plot':
            df[selected_columns].plot(kind='hist', ax=ax)
        elif plot_type == 'Count Plot':
            df[selected_columns].value_counts().plot(kind='bar', ax=ax)

        # Adjust label sizes
        ax.tick_params(axis='x', labelsize=10)  # Adjust x-axis label size
        ax.tick_params(axis='y', labelsize=10)  # Adjust y-axis label size

        # Adjust title and axis labels with a smaller font size
        plt.title(f'{plot_type} of {", ".join(selected_columns)}', fontsize=12)
        plt.xlabel(", ".join(selected_columns), fontsize=10)
        plt.ylabel('Count', fontsize=10)

        # Show the results
        st.pyplot(fig) 

    # Get the total number of items in the database
    total_items = len(rows)
    # Calculate the stock status based on the total number of items
    stock_status = "Increase stock" if total_items < 10 else "Stock is sufficient"
    
    # Display the response
    st.subheader("Response:")
    for row in rows:
        st.write(row)
        
    # Send SMS to the manager
    message = f"Dear {manager_name}, your stock status has been updated. {stock_status}. Total items in database: {total_items}. Please check your inventory.\n\nResponse: {rows}"
    sms_response = sms.send(message, [manager_phone_number])
    
    st.write(f"SMS sent to {manager_name} at {manager_phone_number}")