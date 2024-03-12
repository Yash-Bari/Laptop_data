import os
import shutil
import streamlit as st
import pandas as pd
from zipfile import ZipFile
import base64

# Set page title
st.set_page_config(page_title="Laptop Form", layout="wide")

# Function to create the form
def laptop_form():
    st.subheader("Enter Laptop Details")
    
    # Input fields for laptop details
    laptop_name = st.text_input("Laptop Name")
    specification = st.text_input("Specification")
    price = st.number_input("Price", min_value=0.0)
    categories = st.selectbox("Categories", ["Gaming", "Business", "Home", "Others"])
    images = st.file_uploader("Upload Images (Multiple files supported)", accept_multiple_files=True)
    
    # Submit button
    if st.button("Submit"):
        # Convert images to list of file names
        image_names = [image.name for image in images]
        
        # Create dictionary with laptop details
        laptop_data = {
            "Laptop Name": laptop_name,
            "Specification": specification,
            "Price": price,
            "Categories": categories,
            "Images": image_names
        }
        
        # Append laptop data to CSV file
        df = pd.DataFrame([laptop_data])
        df.to_csv("laptop_data.csv", mode="a", header=not st.session_state.csv_exists, index=False)
        
        # Create folder for images
        folder_name = f"{laptop_name}_{df.index[0]}"
        os.makedirs(folder_name, exist_ok=True)
        
        # Save images to folder
        for image in images:
            with open(os.path.join(folder_name, image.name), "wb") as f:
                f.write(image.getbuffer())
        
        # Mark that CSV file exists
        st.session_state.csv_exists = True
        
        # Display success message
        st.success("Laptop details saved successfully!")

# Function to export CSV and images
def export_data():
    # Copy images folders to 'images' directory
    images_folder = "images"
    os.makedirs(images_folder, exist_ok=True)
    for folder in os.listdir():
        if os.path.isdir(folder) and folder != images_folder:
            shutil.copytree(folder, os.path.join(images_folder, folder))
    
    # Zip images folder
    with ZipFile('images.zip', 'w') as zipf:
        for root, dirs, files in os.walk(images_folder):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), images_folder))
    
    # Display download links
    st.markdown(f"### Export Data")
    st.markdown(get_binary_file_downloader_html("laptop_data.csv", "CSV"), unsafe_allow_html=True)
    st.markdown(get_binary_file_downloader_html("images.zip", "Images ZIP"), unsafe_allow_html=True)

# Function to generate a download link for a file
def get_binary_file_downloader_html(file_path, file_label):
    with open(file_path, "rb") as file:
        data = file.read()
    b64_data = base64.b64encode(data).decode()
    href = f"<a href='data:file/txt;base64,{b64_data}' download='{file_path}'>{file_label}</a>"
    return href

# Check if CSV file exists
if "csv_exists" not in st.session_state:
    st.session_state.csv_exists = False

# Display form
laptop_form()

# Export data
if st.button("Export Data"):
    export_data()
