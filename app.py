import streamlit as st
import tempfile
import os
from pathlib import Path
import json

from automatic_metadata_generator import generate_metadata_from_file, metadata_exporter, create_metadata_visualization

st.set_page_config(page_title="📄 Metadata Extractor", layout="wide")
st.title("📄 Document Metadata Extractor")
st.markdown("Upload a document to extract metadata, view it, and download as JSON.")

uploaded_file = st.file_uploader(
    "Choose a file...", 
    type=['pdf', 'docx', 'txt', 'jpg', 'jpeg', 'png']
)

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as temp_file:
        temp_file.write(uploaded_file.read())
        file_path = temp_file.name

    st.success(f"📁 File uploaded: {uploaded_file.name}")

    if st.button("⚙️ Process Document"):
        st.info("Processing started... Please wait ⏳")

        # Run your metadata extraction function
        metadata = generate_metadata_from_file(file_path, save_results=True, visualize=True)

        if metadata:
            st.success("✅ Metadata extraction completed!")

            st.subheader("📋 Extracted Metadata")
            st.json(metadata)

            # Download button
            json_output = metadata_exporter.export_to_json(metadata, pretty_print=True)
            st.download_button(
                label="⬇️ Download Metadata as JSON",
                data=json_output,
                file_name=f"metadata_{Path(uploaded_file.name).stem}.json",
                mime="application/json"
            )

            # Visualization (Streamlit compatible)
            st.subheader("📊 Metadata Visualizations")
            create_metadata_visualization(metadata)
        else:
            st.error("❌ Metadata extraction failed.")

        # Optional cleanup
        try:
            os.remove(file_path)
        except Exception as e:
            st.warning(f"Could not delete temp file: {e}")
