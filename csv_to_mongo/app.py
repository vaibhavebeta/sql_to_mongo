import streamlit as st
import pandas as pd
import os
import json
from mongo_connection import get_database


db = get_database()
st.title("CSV File Uploader and Viewer")
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        
        file_name = os.path.splitext(uploaded_file.name)[0]
        
        collection = db[file_name]
        
        data = df.to_dict(orient="records")
        
        if data:  
            collection.insert_many(data)
            st.success(f"✅ Data inserted into MongoDB collection: `{file_name}`")

        st.write("### Preview of Uploaded CSV File:")
        st.dataframe(df.style.set_properties(**{'background-color': '#f5f5f5',
                                                'border-color': 'black',
                                                'color': 'black'}))
        
        # Fetch data from MongoDB for download
        saved_data = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB ObjectId
        json_data = json.dumps(saved_data, indent=4)

        # Provide a Download Button
        st.download_button(
            label="📥 Download Data as JSON",
            data=json_data,
            file_name=f"{file_name}.json",
            mime="application/json"
        )

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
