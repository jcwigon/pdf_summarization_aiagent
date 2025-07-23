import streamlit as st
import PyPDF2
import requests

st.set_page_config(page_title="Agent PDF AI", page_icon="📄")
st.title("📄 Agent AI do streszczenia PDF")

st.info(
    """
    **Jak korzystać z aplikacji?**
    1. Załóż darmowe konto lub zaloguj się na [DeepSeek Platform](https://platform.deepseek.com/api-keys).
    2. Po zalogowaniu kliknij "API Keys" (u góry strony).
    3. Wygeneruj nowy klucz lub skopiuj już istniejący.
    4. Wklej swój klucz API poniżej.
    """
)

api_key = st.text_input("Wklej swój klucz DeepSeek API:", type="password")

uploaded_file = st.file_uploader("Wrzuć plik PDF", type=["pdf"])

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def summarize_with_deepseek_api(text, api_key):
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}"}
    prompt = "Streszcz ten dokument po polsku w punktach:\n" + text[:3500]
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "Jesteś pomocnym asystentem AI."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, json=payload, headers=headers)
    try:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Błąd generowania streszczenia: {e}\n\nSzczegóły: {response.text}"

if uploaded_file and api_key:
    with st.spinner("Wyciąganie tekstu z PDF..."):
        text = extract_text_from_pdf(uploaded_file)
        st.subheader("Tekst z PDF:")
        st.write(text[:1000] + ("..." if len(text) > 1000 else ""))

    if text.strip():
        with st.spinner("Generowanie streszczenia przez DeepSeek..."):
            summary = summarize_with_deepseek_api(text, api_key)
            st.subheader("Streszczenie AI (DeepSeek):")
            # Formatowanie w punkty (jeśli nie ma bulletów, to rozbij na zdania)
            if '\n' in summary:
                points = [line.strip() for line in summary.split('\n') if line.strip()]
            else:
                points = [s.strip() for s in summary.split('. ') if s.strip()]
            for point in points:
                st.markdown(f"- {point}")
    else:
        st.warning("Nie udało się wyciągnąć tekstu z PDF-a.")
elif uploaded_file and not api_key:
    st.warning("Wklej swój klucz DeepSeek API, aby wygenerować streszczenie.")



