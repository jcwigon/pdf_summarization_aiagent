import streamlit as st
import PyPDF2
from transformers import pipeline

st.set_page_config(page_title="Agent PDF AI", page_icon="📄")
st.title("📄 Agent AI do streszczenia PDF")

uploaded_file = st.file_uploader("Wrzuć plik PDF", type=["pdf"])

@st.cache_resource
def get_summarizer():
    return pipeline("summarization", model="deepseek-ai/deepseek-llm-7b-chat")

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def summarize_text(text):
    summarizer = get_summarizer()
    max_chunk_len = 2048
    chunks = [text[i:i+max_chunk_len] for i in range(0, len(text), max_chunk_len)]
    summary = ""
    for chunk in chunks:
        result = summarizer(chunk, max_length=180, min_length=50, do_sample=False)
        summary += result[0]['summary_text'].strip() + "\n\n"
    return summary.strip()

if uploaded_file:
    with st.spinner("Wyciąganie tekstu z PDF..."):
        text = extract_text_from_pdf(uploaded_file)
        st.subheader("Tekst z PDF:")
        st.write(text[:1000] + ("..." if len(text) > 1000 else ""))

    if text.strip():
        with st.spinner("Generowanie streszczenia..."):
            summary = summarize_text(text)
            st.subheader("Streszczenie AI:")
            points = [s.strip() for s in summary.replace('\n', ' ').split('. ') if s.strip()]
            for point in points:
                st.markdown(f"- {point}.")
    else:
        st.warning("Nie udało się wyciągnąć tekstu z PDF-a.")


