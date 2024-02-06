import streamlit as st
from PIL import Image
import cv2
import numpy as np

import os

import google.generativeai as genai
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv, dotenv_values  # we can use load_dotenv or dotenv_values both perform the same task

load_dotenv()

# print(os.getenv("MY_SECRET_KEY"))

genai.configure(api_key=os.getenv("MY_SECRET_KEY")) 

# Set up the model
generation_config = {
  "temperature": 0.9,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 1024,
}

def main():
    st.title("Object Finder 🔍")   
    # Create a folder to store uploaded files
    upload_folder = "uploaded_images"
    os.makedirs(upload_folder, exist_ok=True)

    # Upload image through Streamlit
    uploaded_image = st.file_uploader("Choose an image ...", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
      image_path = os.path.join(upload_folder, uploaded_image.name)
      with open(image_path, "wb") as f:
        f.write(uploaded_image.getbuffer())
        # Display the uploaded image
        st.image(uploaded_image, caption="Uploaded Image.", use_column_width=True)

        # Process the image (example: get image dimensions)
        image = Image.open(uploaded_image)
        width, height = image.size
        st.write("Image Dimensions:", f"{width}x{height}")

        if st.button("Identify the objects"):

            st.success("Detecting...")
            company = "Dove"
            prompt_template = f'''You are a field officer for {company} company. You are there at the store to analyse product placement. Identify the products in the image and for every product make a JSON format with the keys as product_name, count. I have explained the keys below product_name - The product name is the biggest name written on the image. count - The number of products of that product_name in the image.  Output the JSON in a formatted manner'''
      

            vision_model = genai.GenerativeModel('gemini-pro-vision')
            response = vision_model.generate_content([prompt_template,image])
            # prompt_template1 = f'''You are a field officer for {company} company. You are there at the store to analyse product placement. Identify every product unit in the image label it as brand name and a number and for every unit make a JSON format with the keys as product_label, shelf number. I have explained the keys below product_name - The product name is the biggest name written on the image. count - The number of products of that product_name in the image.  Output the JSON in a formatted manner'''
            
            # response1 = vision_model.generate_content([prompt_template1,image])
            # Provide the product names, count, shelf number in a JSON format.
            # prompt = f"Identify the products in the image {uploaded_image.name}. Determine their relative positions considering factors like eye-level, visibility, lighting, bottom placement, and proximity to corners. Provide the product names, count, shelf number, and their positions in a JSON format."


            
            st.write("The objects detected are \n", response.text)
            im = cv2.imread(uploaded_image, cv2.IMREAD_GRAYSCALE)
            vis = np.std(im)
            st.write(f"Visibility Score: {vis}")


if __name__ == "__main__":
    main()
