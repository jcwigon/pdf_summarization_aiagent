import streamlit as st
import PyPDF2
from transformers import pipeline

st.set_page_config(page_title="Agent PDF AI (open source)", page_icon="📄")
st.title("📄 Agent AI do streszczenia PDF (open source, bez klucza!)")

uploaded_file = st.file_uploader("Wrzuć plik PDF", type=["pdf"])

@st.cache_resource
def get_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def summarize_text_local(text):
    summarizer = get_summarizer()
    # Dziel tekst na fragmenty max 1024 tokeny (limity BART)
    max_chunk_len = 1024
    chunks = [text[i:i+max_chunk_len] for i in range(0, len(text), max_chunk_len)]
    summary = ""
    for chunk in chunks:
        result = summarizer(chunk, max_length=130, min_length=30, do_sample=False)
        summary += result[0]['summary_text'] + " "
    return summary.strip()

if uploaded_file:
    with st.spinner("Wyciąganie tekstu z PDF..."):
        text = extract_text_from_pdf(uploaded_file)
        st.subheader("Tekst z PDF:")
        st.write(text[:1000] + ("..." if len(text) > 1000 else ""))

    if text.strip():
        with st.spinner("Generowanie streszczenia (może chwilę potrwać)..."):
            summary = summarize_text_local(text)
            st.subheader("Streszczenie AI (open source):")
            st.write(summary)
    else:
        st.warning("Nie udało się wyciągnąć tekstu z PDF-a.")

