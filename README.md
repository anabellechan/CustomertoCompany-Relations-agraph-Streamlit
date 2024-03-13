# CustomertoCompany-Relations-agraph-Streamlit
This is a project that drafts out common companies among a list of customers on an agraph in Streamlit.

Features:
-Sidebar for file uploading.  
-Checks file extension and gives error if wrong file format (not an .xlsx)  
-Able to ingest excel format   
-Parse the content of excel using pandas read_excel   
-Write phone number regex for sg numbers eg. +65 to extract from excel content across different tabs   
-Able to upload a json data and view the displayed customer-to-companies relationship graph.  
