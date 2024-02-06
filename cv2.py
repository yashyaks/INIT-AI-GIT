import streamlit as st
from PIL import Image
import os
import json

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
    st.title("Shelf Analysis App 🛒")
    
    disclaimer_message = "This app analyzes the shelf, counts products, assesses eye-level visibility and lighting conditions, and identifies the brand of the image."

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

        if st.button("Analyze Shelf"):
            st.success("Analyzing...")

            vision_model = genai.GenerativeModel('gemini-pro-vision')
            response = vision_model.generate_content(["Analyze shelf, count products, assess eye-level visibility, and identify brand in json format.", image])

            # Try to parse the response
            try:
                analysis_result = json.loads(response.text)
            except json.JSONDecodeError as e:
                st.error(f"Error decoding JSON response: {e}")
                st.write("Response:", response.text)
                return

            # Parse the response to extract information
            shelf_info = analysis_result.get("shelf_info", {})
            products = analysis_result.get("products", [])
            brand = analysis_result.get("brand", "Unknown")

            # Display the analysis result
            st.write("Analysis Result:")
            st.write("- Shelf Number:", shelf_info.get("shelf_number", "Unknown"))
            st.write("- Product Count:", len(products))

            # Analyze placement based on area ratio
            placement_analysis = analyze_placement(products)

            # Display the placement analysis
            st.write("- Placement Analysis:")
            for analysis in placement_analysis:
                st.write(f"  - {analysis['product_name']}: {analysis['placement_status']}")

            st.write("- Eye-Level Visibility Assessment:", shelf_info.get("eye_level_visibility", "Unknown"))
            st.write("- Lighting Conditions:", shelf_info.get("lighting_conditions", "Unknown"))
            st.write("- Brand of the Image:", brand)

            st.success("Analysis completed!")

if __name__ == "__main__":
    main()
