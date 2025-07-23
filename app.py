
import streamlit as st
import PyPDF2
import openai

st.set_page_config(page_title="Agent PDF AI", page_icon="📄")
st.title("📄 AI Agent do analizy PDF")

openai_api_key = st.text_input("Wklej swój klucz OpenAI API:", type="password")

uploaded_file = st.file_uploader("Wrzuć plik PDF", type=["pdf"])

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def summarize_text(text, openai_api_key, prompt="Streszcz ten dokument:"):
    if not openai_api_key:
        return "Brak klucza OpenAI!"
    client = openai.OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Jesteś pomocnym asystentem AI."},
            {"role": "user", "content": prompt + "\n\n" + text[:3000]}  # Uwaga na limity!
        ]
    )
    return response.choices[0].message.content

if uploaded_file and openai_api_key:
    with st.spinner("Wyciąganie tekstu z PDF..."):
        text = extract_text_from_pdf(uploaded_file)
        st.subheader("Tekst z PDF:")
        st.write(text[:1000] + ("..." if len(text) > 1000 else ""))
    with st.spinner("Generowanie streszczenia..."):
        summary = summarize_text(text, openai_api_key)
        st.subheader("Streszczenie AI:")
        st.write(summary)
