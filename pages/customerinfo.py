import glob
import pandas as pd
import streamlit as st
import psycopg2

st.set_page_config(layout="wide")

##Connect to postgres
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="abc123",
    host="localhost"
)

# Create a cursor object
cur = conn.cursor()

# Execute a query to fetch all rows from the customerdata table
cur.execute("SELECT * FROM customerdata;")

# Fetch all the rows from the cursor
rows = cur.fetchall()
columns = [desc[0] for desc in cur.description]
df = pd.DataFrame(rows, columns=columns)


# Close the cursor and connection
st.header("Customer's Table")
st.dataframe(data=df, width=2000, height=1000)

# Create a cursor object
cur = conn.cursor()

# Execute a query to fetch rows from the customerdata table where phone1 and phone2 start with +65
cur.execute("SELECT firstname, lastname, phone1, phone2 FROM customerdata WHERE phone1 LIKE '+65%' OR phone2 LIKE '+65%';")

# Fetch all the rows from the cursor
rows = cur.fetchall()
columns = [desc[0] for desc in cur.description]
phonedf = pd.DataFrame(rows, columns=columns)

# Close the cursor and connection
cur.close()
conn.close()

st.header("+65 Ext. Local Number Table")
st.dataframe(data=phonedf, width=2000, height=400)



# To take in Excel and concat all tabs together

# def load_phnumbers():
#     excel_files = glob.glob('.\data\customers-20 new.xlsx')
#     # Initialize an empty list to store all DataFrames
#     all_dataframes = []
#     all_phone_numbers = []

#     for file in excel_files:
#         # Read all sheets from the Excel file
#         all_sheets_dict = pd.read_excel(file, sheet_name=None)
        
#         # Iterate through the dictionary and append each DataFrame to the list
#         for sheet_name, df in all_sheets_dict.items():
#             all_dataframes.append(df)

#             # Check for the presence of phone number columns and extract them
#             if 'Phone' in df.columns or 'Phone 1' and 'Phone 2' in df.columns:
#                 if 'Phone' in df.columns:
#                     phone_numbers = df['Phone'].tolist()
#                     all_phone_numbers.extend(phone_numbers)
#                 if 'Phone 1' and 'Phone 2' in df.columns:
#                     phone_numbers_1 = df['Phone 1'].tolist()
#                     phone_numbers_2 = df['Phone 2'].tolist()
#                     all_phone_numbers.extend(phone_numbers_1+ phone_numbers_2)
#     # Concatenate all DataFrames into a single DataFrame
#     combined_df = pd.concat(all_dataframes, ignore_index=True)
#     # combined_df.to_excel('combined_data.xlsx', index=False, engine='xlsxwriter')
#     combined_df.to_csv('combined_data.csv', index=False)
#     print("Combined DataFrame", combined_df)
#     print("All Phone Numbers", len(all_phone_numbers)) #phone 1 and phone 2 gives more numbers
#     return all_phone_numbers, combined_df

# phone_numbers, combined_df = load_phnumbers()