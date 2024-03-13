import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import sqlalchemy.exc
import glob


# db_config = st.secrets["postgresql"]

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="abc123",
    host="localhost"
)

def is_excel_file(uploaded_file):
    if uploaded_file is not None:
        return uploaded_file.type in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']
    return False


uploaded_file = st.file_uploader("Upload your Excel file here...", type=['xlsx']) #check once
all_dataframes = []

# excel_files = glob.glob(uploaded_file)

# # Button to trigger file processing
# if st.button('Process file'):
#     for file in excel_files:
#     ### Concatenating all excel tabs first ####
#     # Read all sheets from the Excel file
#         all_sheets_dict = pd.read_excel(file, sheet_name=None)
#     # Iterate through the dictionary and append each DataFrame to the list
#     for sheet_name, df in all_sheets_dict.items():
#         all_dataframes.append(df)
# # concatenate all dataframes
#     combined_df = pd.concat(all_dataframes, ignore_index=True)
#     print("hellos", combined_df)

if st.button('Process file'):
    if uploaded_file is not None and is_excel_file(uploaded_file): #check twice
            try:
                all_sheets_dict = pd.read_excel(uploaded_file, sheet_name=None)
                for sheet_name, df in all_sheets_dict.items():
                    all_dataframes.append(df)
        
                # Concatenate all dataframes
                combined_df = pd.concat(all_dataframes, ignore_index=True)
                print("hellos", combined_df)
                combined_df.rename(columns={'Index': 'index', 'Customer Id': 'customerid','First Name': 'firstname','Last Name': 'lastname','Company': 'company','City': 'city' ,'Country': 'country','Phone 1': 'phone1','Phone 2': 'phone2','Email': 'email','Subscription Date': 'subscriptiondate','Website': 'website' }, inplace=True)
                # Create a SQLAlchemy engine
                engine = create_engine("postgresql+psycopg2://postgres:abc123@localhost:5432/postgres")
                # Insert the DataFrame into a new table
                combined_df.to_sql('customerdata', engine, if_exists='append', index=False)
                st.success("Data has been successfully uploaded and appended to the table.")
                st.write(combined_df)
                
                # Close the connection
                conn.close()
            except Exception as e:
                st.error(f"An error occurred: \n {e}")
    else:
            st.error("Please upload an Excel file.")
# else:
#     st.error("Please upload a file.")