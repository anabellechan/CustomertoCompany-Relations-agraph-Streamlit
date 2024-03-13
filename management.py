import streamlit as st
import json
from streamlit_agraph import agraph, Node, Edge, Config
import numpy as np
import pandas as pd
from time import time
import glob
import psycopg2

st.title('Companies & their Management')

@st.cache_data
def load_data_from_postgres():
    # Replace the connection parameters with your PostgreSQL server details
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="abc123"
    )
    
    query = "SELECT * FROM customerdata;"  # Replace with your SQL query
    df = pd.read_sql_query(query, conn)
    
    conn.close()
    return df


df = load_data_from_postgres()

unique_names = df['firstname'].unique()
unique_companies = df['company'].unique()


#Sidebar
st.sidebar.write("Filters")
filter_companies = st.sidebar.multiselect("Select Organisations",
                                     unique_companies,
                                     max_selections=5,
                                     default=unique_companies[:5]) #list of 5 organizations

filtered_df = df[df['company'].isin(filter_companies)]
mgmt_data = filtered_df.to_json(orient='values')
dict_convert = json.loads(mgmt_data)
#st.write(dict_convert)

def make_graph(dict_convert,position_show=False):
    nodes = []
    edges = []
    execs = []
    companies = []

    for data in dict_convert: 
        #st.write(data)
        firstname = data[2]
        company = data[4]

#creating graph instance of nodes and edges
        if firstname not in execs:
            nodes.append(Node(id=firstname,symbolType='diamond',color='#FDD00F'))
            execs.append(firstname)

        if company not in companies:
            nodes.append(Node(id=company,label=company,color="#07A7A6"))
            companies.append(company)
        
        position = f"{data[4]} of"

        if position_show: 
            edges.append(Edge(source=firstname,target=company,label=position))
        else:
            edges.append(Edge(source=firstname,target=company))

    return [nodes, edges]

config = Config(width=750,
                    height=950,
                    directed=True,
                    physics=True,
                    hierarchical=False,
                    highlightColor='#FF00FF',
                    nodeHighlightBehavior=True,
                    node={'labelProperty':'label','renderLabel':False}) #adjust height and width of the graphs

position_show = st.sidebar.checkbox('Show Position')
#st.write(position_show)
filter_nodes, filter_edges = make_graph(dict_convert,position_show)

return_value = agraph(nodes = filter_nodes, 
                      edges = filter_edges, 
                      config = config)
