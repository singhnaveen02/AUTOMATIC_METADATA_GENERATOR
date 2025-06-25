import streamlit as st
import tempfile
import os
import json
from automatic_metadata_generator import generate_metadata_from_file

st.set_page_config(page_title="Automatic Metadata Generator", layout="wide")
st.title("📄 Automatic Metadata Generator")

uploaded_file = st.file_uploader(
    "Upload your document (PDF, DOCX, TXT, PNG, JPG, JPEG)", 
    type=["pdf", "docx", "txt", "png", "jpg", "jpeg"]
)

metadata = None

if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
        temp_file.write(uploaded_file.read())
        file_path = temp_file.name

    if st.button("⚙️ Generate Metadata"):
        with st.spinner("Processing... please wait ⏳"):
            metadata = generate_metadata_from_file(file_path, save_results=True, visualize=False)

        if metadata:
            st.success("✅ Metadata generated successfully!")

            st.subheader("📋 Document Info")
            doc_info = metadata.get('document_info', {})
            st.write(f"**Title:** {doc_info.get('title', 'N/A')}")
            st.write(f"**Filename:** {doc_info.get('filename', 'N/A')}")
            st.write(f"**File Type:** {doc_info.get('file_type', 'N/A')}")
            st.write(f"**Processing Date:** {doc_info.get('processing_date', 'N/A')}")

            st.subheader("🏷️ Keywords")
            st.write(", ".join(metadata.get("semantic_metadata", {}).get("keywords", [])))

            st.subheader("📝 Summary")
            st.write(metadata.get("semantic_metadata", {}).get("summary", "No summary available"))

            st.subheader("📌 Key Sentences")
            for sent in metadata.get("semantic_metadata", {}).get("key_sentences", []):
                st.markdown(f"- {sent}")

            st.subheader("📊 Quality Metrics")
            quality = metadata.get("quality_metrics", {})
            st.metric(label="Extraction Confidence", value=f"{quality.get('extraction_confidence', 0)*100:.1f}%")
            st.metric(label="Text Quality Score", value=f"{quality.get('text_quality_score', 0)*100:.1f}%")
            st.metric(label="Completeness Score", value=f"{quality.get('completeness_score', 0)*100:.1f}%")

            st.subheader("📄 Full Metadata JSON")
            st.json(metadata)

            json_str = json.dumps(metadata, indent=2)
            st.download_button(
                label="⬇️ Download Metadata as JSON",
                data=json_str,
                file_name=f"metadata_{uploaded_file.name.split('.')[0]}.json",
                mime="application/json"
            )
        else:
            st.error("❌ Failed to generate metadata.")
