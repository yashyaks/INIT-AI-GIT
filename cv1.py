import streamlit as st
from PIL import Image
import os
import json
import numpy as np

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("MY_SECRET_KEY"))

generation_config = {
    "temperature": 0.9,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 1024,
}

def analyze_placement(products):
    # Define a threshold for acceptable area ratio
    threshold = 0.01  # You may need to adjust this based on your specific use case

    placement_analysis = []

    for product in products:
        area_ratio = product.get("area_ratio", 0.0)

        if area_ratio >= threshold:
            placement_analysis.append({
                "product_name": product.get("product_name", "Unknown"),
                "count": product.get("count", 0),
                "placement_status": "Properly Placed"
            })
        else:
            placement_analysis.append({
                "product_name": product.get("product_name", "Unknown"),
                "count": product.get("count", 0),
                "placement_status": "Improper Placement"
            })

    return placement_analysis

def main():
    st.title("Object Finder 🔍")
    
    disclaimer_message = "This is an object detection model, so preferably use images containing different objects, tools for best results 🙂"

    # Hide the disclaimer initially
    st.write("")

    # Show the disclaimer if the button is clicked
    with st.expander("Disclaimer ⚠️", expanded=False):
        st.markdown(disclaimer_message)
    
    # Upload image through Streamlit
    uploaded_image = st.file_uploader("Choose an image ...", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        # Display the uploaded image
        st.image(uploaded_image, caption="Uploaded Image.", use_column_width=True)

        # Process the image
        image = Image.open(uploaded_image)
        width, height = image.size
        st.write("Image Dimensions:", f"{width}x{height}")

        if st.button("Identify the objects"):
            st.success("Detecting...")

            vision_model = genai.GenerativeModel('gemini-pro-vision')
            response = vision_model.generate_content(["Provide the product names, count, shelf number in a JSON format.", image])

            # Parse the response to extract information
            try:
                products = json.loads(response.text)
            except json.JSONDecodeError:
                st.error("Error decoding JSON response.")
                return

            # Analyze placement based on area ratio
            placement_analysis = analyze_placement(products)

            # Display the analysis
            st.write("Placement Analysis:")
            for analysis in placement_analysis:
                st.write(f"- {analysis['product_name']}: {analysis['placement_status']}")

            st.success("Analysis completed!")

if __name__ == "__main__":
    main()
