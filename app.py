import streamlit as st
import PyPDF2
import requests

st.set_page_config(page_title="Agent PDF AI", page_icon="📄")
st.title("📄 Agent AI do ekstrakcji informacji z PDF (Groq API)")

st.info(
    """
    **Jak korzystać z aplikacji?**
    1. Załóż darmowe konto lub zaloguj się na [Groq Platform](https://console.groq.com/keys).
    2. Wygeneruj nowy klucz (API Key).
    3. Wklej swój klucz API poniżej i kliknij **Załaduj klucz**.
    """
)

if 'api_key_loaded' not in st.session_state:
    st.session_state['api_key_loaded'] = False
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ""

api_key = st.text_input("Wklej swój klucz Groq API:", type="password", value=st.session_state['api_key'])
key_loaded = st.button("Załaduj klucz")

if key_loaded and api_key:
    st.session_state['api_key_loaded'] = True
    st.session_state['api_key'] = api_key

if st.session_state['api_key_loaded']:
    st.success("✅ API key załadowany")
    st.markdown("---")
    uploaded_file = st.file_uploader("Wrzuć plik PDF", type=["pdf"])

    def extract_text_from_pdf(file):
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text

    def extract_key_points_with_groq_api(text, api_key):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        prompt = (
            "Wypisz najważniejsze informacje z dokumentu w punktach i sekcjach po polsku, "
            "bez rozbudowanych opisów – tylko kluczowe dane, fakty, stanowiska, daty, nazwy, wartości itd."
            "\n\nTekst:\n" + text[:6000]
        )
        payload = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 800,
            "temperature": 0.2
        }
        response = requests.post(url, json=payload, headers=headers)
        try:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"❌ Błąd generowania najważniejszych informacji: {e}\n\nSzczegóły: {response.text}"

    def summarize_briefly_with_groq_api(text, api_key):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        prompt = (
            "Stwórz krótkie streszczenie poniższego dokumentu po polsku (3-5 zdań). Podkreśl kluczowe tematy i główny cel dokumentu."
            "\n\nTekst:\n" + text[:6000]
        )
        payload = {
            "model": "llama3-70b-8192",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 350,
            "temperature": 0.3
        }
        response = requests.post(url, json=payload, headers=headers)
        try:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"❌ Błąd generowania streszczenia: {e}\n\nSzczegóły: {response.text}"

    if uploaded_file:
        with st.spinner("Wyciąganie tekstu z PDF..."):
            text = extract_text_from_pdf(uploaded_file)
            st.subheader("Tekst z PDF:")
            st.write(text[:1000] + ("..." if len(text) > 1000 else ""))

        if text.strip():
            # Najważniejsze informacje (punkty)
            with st.spinner("Ekstrakcja najważniejszych informacji..."):
                key_points = extract_key_points_with_groq_api(text, st.session_state['api_key'])
                st.header("Najważniejsze informacje")
                if '\n' in key_points:
                    points = [line.strip() for line in key_points.split('\n') if line.strip()]
                else:
                    points = [s.strip() for s in key_points.split('. ') if s.strip()]
                for point in points:
                    st.markdown(f"- {point}")

            # Streszczenie ogólne
            with st.spinner("Generowanie streszczenia..."):
                summary = summarize_briefly_with_groq_api(text, st.session_state['api_key'])
                st.header("Streszczenie")
                st.write(summary)
        else:
            st.warning("Nie udało się wyciągnąć tekstu z PDF-a.")
else:
    if api_key and not st.session_state['api_key_loaded']:
        st.info("Wklej klucz i kliknij **Załaduj klucz**.")
    elif not api_key and key_loaded:
        st.warning("Wklej klucz przed kliknięciem 'Załaduj klucz'.")





