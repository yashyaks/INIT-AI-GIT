import os
import cv2
import numpy as np
import streamlit as st

def calculate_image_contrast(image_path):
    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Calculate the standard deviation of pixel intensities
    contrast = np.std(image)

    return contrast

def main():
    st.title("Image Contrast Calculator")

    # Create a folder to store uploaded files
    upload_folder = "uploaded_images"
    os.makedirs(upload_folder, exist_ok=True)

    # File uploader to get the image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Save the uploaded file to the folder
        image_path = os.path.join(upload_folder, uploaded_file.name)
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Display the uploaded image
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

        # Calculate and display the contrast value
        contrast_value = calculate_image_contrast(image_path)
        st.write(f"Image contrast: {contrast_value}")

        # Display the path of the uploaded image
        st.write(f"Uploaded image path: {image_path}")

if __name__ == "__main__":
    main()
