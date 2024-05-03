import streamlit as st
import pandas as pd
import requests
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

# Initialize ChatterBot instance
chatbot = ChatBot("Internal Website Chatbot")

def fetch_training_data_from_api(api_url):
    """
    Fetch training data from the internal website's API
    """
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch training data from the API.")
            return []
    except Exception as e:
        st.error(f"Error fetching training data from the API: {e}")
        return []

def train_chatbot_with_api_data(chatbot, api_data):
    """
    Train the chatbot with data fetched from the API
    """
    trainer = ListTrainer(chatbot)
    for item in api_data:
        trainer.train([item['question'], item['answer']])

def generate_column_analysis(dataframe, column):
    """
    Function to generate column-level analysis
    """
    st.subheader(f"Analysis for column: {column}")
    
    # Display basic statistics
    st.write("Basic Statistics:")
    st.write(dataframe[column].describe())
    
    # Display unique values
    st.write("Unique Values:")
    st.write(dataframe[column].unique())
    
    # Display value counts
    st.write("Value Counts:")
    st.write(dataframe[column].value_counts())
    
    # Add more analysis here as needed

def main():
    """
    Main function to run the Streamlit app
    """
    st.title("Column-level Analysis Generator & Chatbot")
    
    # Option to upload file
    uploaded_file = st.file_uploader("Upload file", type=["csv", "xlsx", "xls"])
    
    # Option to provide URL or API endpoint
    option = st.radio("Choose option:", ("Upload File", "Provide API Endpoint"))
    
    if option == "Upload File" and uploaded_file is not None:
        # Handle file upload
        # Read the uploaded file and generate column analysis
        file_ext = uploaded_file.name.split('.')[-1]
        if file_ext.lower() == 'csv':
            dataframe = pd.read_csv(uploaded_file)
        elif file_ext.lower() in ['xlsx', 'xls']:
            dataframe = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please upload a CSV, Excel (xls or xlsx) file.")
            return
        
        st.write(dataframe.head())  # Display the first few rows of the dataframe
        
        # Select column for analysis
        selected_column = st.selectbox("Select column for analysis", dataframe.columns)
        
        # Generate analysis for selected column
        generate_column_analysis(dataframe, selected_column)
    
    elif option == "Provide API Endpoint":
        # Option to provide API endpoint
        api_url = st.text_input("Enter API Endpoint:")
        if st.button("Fetch Training Data"):
            # Fetch training data from the API
            api_data = fetch_training_data_from_api(api_url)
            if api_data:
                # Train chatbot with fetched data
                train_chatbot_with_api_data(chatbot, api_data)
                st.success("Chatbot trained successfully with data from the API.")
            else:
                st.warning("No training data fetched from the API.")
    
    # Chat functionality
    st.subheader("Chat")
    user_input = st.text_input("You:", "")
    if st.button("Send"):
        bot_response = str(chatbot.get_response(user_input))
        st.write("Bot:", bot_response)

if __name__ == "__main__":
    main()
