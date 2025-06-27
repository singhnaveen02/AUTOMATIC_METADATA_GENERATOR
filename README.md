# AUTOMATIC_METADATA_GENERATOR

This Streamlit app processes documents (PDF, DOCX, TXT, images) to generate rich metadata including:
- Keywords
- Summary
- Entities
- Text quality metrics

## How to Run

```bash
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')"
streamlit run app.py

