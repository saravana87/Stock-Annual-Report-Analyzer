import streamlit as st
import pandas as pd
from nifty50_scrape import fetch_nifty50_data  # Import the function from nifty50_scrape.py
from datetime import datetime


def main():
   # Set page config
   st.set_page_config(page_title="Stock Analysis Dashboard", layout="wide")
   
   # Sidebar
   st.sidebar.title("Navigation")
   menu_selection = st.sidebar.radio(
       "Choose a page",
       ["Data Input", "Data Overview", "Stock Analysis", "Chat"]
   )
   
   # Main content based on selection
   if menu_selection == "Data Input":
       show_data_input_page()
   elif menu_selection == "Data Overview":
       show_data_overview_page()
   elif menu_selection == "Stock Analysis":
       show_analysis_page()
   else:  # Chat page
       show_chat_page()

def show_data_input_page():
   st.title("Data Input")
   
   # Two columns for Nifty 50 and CSV upload
   col1, col2 = st.columns(2)
   
   with col1:
       st.subheader("Nifty 50 Crawler")
       if st.button("Download Nifty 50 Data"):
           # Here we'll integrate your crawler code
        st.info("Starting download...")
        try:                
            nifty_data = fetch_nifty50_data()  # Call the crawler function
            nifty_data.dropna(how="all", inplace=True)
            st.success("Data download complete!")            
            # Display data or provide download
            st.write(nifty_data.dropna())  # Display in Streamlit
            # If data is in a DataFrame, you can add a download button:
            csv = nifty_data.to_csv(index=False)
            current_date = datetime.now().strftime('%Y%m%d_%H%M')        
            st.download_button("Download CSV", csv, f"nifty50_data_{current_date}.csv", "text/csv")    
        except Exception as e:
            st.error(f"An error occurred: {e}")            
   
   with col2:
       st.subheader("Upload CSV")
       uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
       if uploaded_file is not None:
           try:
               df = pd.read_csv(uploaded_file)
               if 'Symbol' not in df.columns:
                   st.error("CSV must contain 'Symbol' column")
               else:
                   st.success("File uploaded successfully!")
                   st.write("Preview of uploaded data:")
                   st.dataframe(df.head())
                   # Store the dataframe in session state
                   st.session_state['stock_data'] = df
           except Exception as e:
               st.error(f"Error reading file: {e}")

def show_data_overview_page():
    st.title("Data Overview")
    
    uploaded_excel = st.file_uploader("Upload an Excel file", type=["xlsx"])
    
    if uploaded_excel:
        try:
            # Load the Excel file
            excel_data = pd.ExcelFile(uploaded_excel)
            
            # Display sheet names
            st.write("Sheet names:")
            st.write(excel_data.sheet_names)
            
            # Option to select a sheet to view
            sheet_name = st.selectbox("Select a sheet to preview", excel_data.sheet_names)
            
            # Load and display the selected sheet
            df = excel_data.parse(sheet_name)
            st.write("Data preview:")
            st.dataframe(df.head(10))
            
            # Store the dataframe in session state
            st.session_state['stock_data'] = df
            
        except Exception as e:
            st.error(f"Error reading Excel file: {e}")
    else:
        st.warning("No data loaded. Please upload an Excel file.")


def show_analysis_page():
   st.title("Stock Analysis")
   
   if 'stock_data' not in st.session_state:
       st.warning("No data loaded. Please load data from the Data Input page.")
       return
   
   # Add your analysis tools here
   st.subheader("Analysis Tools")
   # Add stock selection, charts, etc.

def show_chat_page():
   st.title("Chat Interface")
   
   if 'stock_data' not in st.session_state:
       st.warning("No data loaded. Please load data from the Data Input page.")
       return
   
   # Simple chat interface
   user_input = st.text_input("Ask about your stocks:")
   if user_input:
       st.write(f"You asked: {user_input}")
       # Here we'll add the chat functionality later

if __name__ == "__main__":
   main()