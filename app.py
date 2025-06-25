import streamlit as st
import tempfile
import json
from pathlib import Path
import os

# Import the function and exporter from your main script
from automatic_metadata_generator import generate_metadata_from_file, metadata_exporter

st.set_page_config(page_title="Document Metadata Extractor", layout="wide")
st.title("📄 Document Metadata Extractor")
st.markdown("Upload a document (PDF, DOCX, TXT, JPG, PNG) to extract its metadata.")

uploaded_file = st.file_uploader(
    "Choose a file...",
    type=['pdf', 'docx', 'txt', 'jpg', 'jpeg', 'png']
)

if uploaded_file is not None:
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as temp_file:
        temp_file.write(uploaded_file.getvalue())
        file_path = temp_file.name

    st.success(f"📁 File uploaded: `{uploaded_file.name}`")

    if st.button("⚙️ Process Document"):
        st.info("⏳ Processing... Please wait a moment.")

        # ✅ You asked to keep both save and visualize as TRUE
        metadata = generate_metadata_from_file(file_path, save_results=True, visualize=True)

        if metadata:
            st.success("✅ Processing Complete!")

            st.subheader("📋 Extracted Metadata")
            st.json(metadata)

            json_output = metadata_exporter.export_to_json(metadata, pretty_print=True)
            st.download_button(
                label="⬇️ Download Metadata as JSON",
                data=json_output,
                file_name=f"metadata_{Path(uploaded_file.name).stem}.json",
                mime="application/json"
            )
        else:
            st.error("❌ Failed to extract metadata from the document.")

        # Clean up
        try:
            os.remove(file_path)
        except Exception as e:
            st.warning(f"⚠️ Could not delete temp file: {e}")


# import streamlit as st
# import tempfile
# import os
# import json
# from automatic_metadata_generator import generate_metadata_from_file

# st.set_page_config(page_title="Automatic Metadata Generator", layout="wide")
# st.title("📄 Automatic Metadata Generator")

# uploaded_file = st.file_uploader(
#     "Upload your document (PDF, DOCX, TXT, PNG, JPG, JPEG)", 
#     type=["pdf", "docx", "txt", "png", "jpg", "jpeg"]
# )

# metadata = None

# if uploaded_file:
#     with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
#         temp_file.write(uploaded_file.read())
#         file_path = temp_file.name

#     if st.button("⚙️ Generate Metadata"):
#         with st.spinner("Processing... please wait ⏳"):
#             metadata = generate_metadata_from_file(file_path, save_results=True, visualize=False)

#         if metadata:
#             st.success("✅ Metadata generated successfully!")

#             st.subheader("📋 Document Info")
#             doc_info = metadata.get('document_info', {})
#             st.write(f"**Title:** {doc_info.get('title', 'N/A')}")
#             st.write(f"**Filename:** {doc_info.get('filename', 'N/A')}")
#             st.write(f"**File Type:** {doc_info.get('file_type', 'N/A')}")
#             st.write(f"**Processing Date:** {doc_info.get('processing_date', 'N/A')}")

#             st.subheader("🏷️ Keywords")
#             st.write(", ".join(metadata.get("semantic_metadata", {}).get("keywords", [])))

#             st.subheader("📝 Summary")
#             st.write(metadata.get("semantic_metadata", {}).get("summary", "No summary available"))

#             st.subheader("📌 Key Sentences")
#             for sent in metadata.get("semantic_metadata", {}).get("key_sentences", []):
#                 st.markdown(f"- {sent}")

#             st.subheader("📊 Quality Metrics")
#             quality = metadata.get("quality_metrics", {})
#             st.metric(label="Extraction Confidence", value=f"{quality.get('extraction_confidence', 0)*100:.1f}%")
#             st.metric(label="Text Quality Score", value=f"{quality.get('text_quality_score', 0)*100:.1f}%")
#             st.metric(label="Completeness Score", value=f"{quality.get('completeness_score', 0)*100:.1f}%")

#             st.subheader("📄 Full Metadata JSON")
#             st.json(metadata)

#             json_str = json.dumps(metadata, indent=2)
#             st.download_button(
#                 label="⬇️ Download Metadata as JSON",
#                 data=json_str,
#                 file_name=f"metadata_{uploaded_file.name.split('.')[0]}.json",
#                 mime="application/json"
#             )
#         else:
#             st.error("❌ Failed to generate metadata.")
