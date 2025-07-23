import streamlit as st
import PyPDF2
import requests

st.set_page_config(page_title="Agent PDF AI", page_icon="📄")
st.title("📄 Agent AI do ekstrakcji informacji z PDF")

# --- Cała instrukcja (z obrazkiem) w ramce na jasnym tle
def instruction_box():
    st.markdown(
        """
        <div style="
            border-radius: 18px;
            border: 2px solid #E0E7EF;
            background: #f7faff;
            padding: 1.7em 2em 1.2em 2em;
            margin-bottom: 2.3em;
            box-shadow: 0 3px 18px #0001;
            max-width: 600px;
        ">
            <b style="font-size: 1.10em;">Jak korzystać z aplikacji?</b>
            <ol style="margin-top: 1em; margin-bottom: 1.7em;">
                <li>Załóż darmowe konto lub zaloguj się na 
                    <a href="https://console.groq.com/keys" target="_blank" style="color:#2b68c4;"><b>Groq Platform</b></a>.
                </li>
                <li>
                    Wygeneruj nowy klucz (API Key):<br>
                    <div style="text-align:center;margin-top:0.7em;margin-bottom:0.7em;">
                        <img src="https://raw.githubusercontent.com/jcwigon/pdf_summarization_aiagent/main/Api%20groq.png" width="170" style="border-radius:10px;border:1px solid #eee;box-shadow:0 2px 8px #0001;">
                        <div style="font-size:0.97em;color:#7b8693;margin-top:0.2em;">Przycisk 'Create API Key' na Groq Platform</div>
                    </div>
                </li>
                <li>Wklej swój klucz API poniżej i kliknij <b>Załaduj klucz</b>.</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True
    )

instruction_box()

def nice_box(content, bg="#fff", border="#E0E7EF"):
    st.markdown(
        f"""
        <div style="
            border-radius: 16px;
            border: 2px solid {border};
            background: {bg};
            padding: 1.2em 1.5em;
            margin-bottom: 1.5em;
            font-size: 1.05rem;
            line-height: 1.7;
            box-shadow: 0 3px 16px #0001;
            ">
            {content}
        </div>
        """,
        unsafe_allow_html=True,
    )

if 'api_key_loaded' not in st.session_state:
    st.session_state['api_key_loaded'] = False
if 'api_key' not in st.session_state:
    st.session_state['api_key'] = ""

api_key = st.text_input("Wklej swój klucz Groq API:", type="password", value=st.session_state['api_key'])
key_loaded = st.button("Załaduj klucz")

def clean_api_key(key):
    return ''.join(c for c in key if 32 < ord(c) < 127)

if key_loaded and api_key:
    st.session_state['api_key_loaded'] = True
    st.session_state['api_key'] = clean_api_key(api_key)

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
            "Authorization": f"Bearer {clean_api_key(api_key)}",
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
            "Authorization": f"Bearer {clean_api_key(api_key)}",
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

        tab1, tab2 = st.tabs(["📄 Podgląd PDF", "🤖 Ekstrakcja AI"])

        with tab1:
            st.subheader("Tekst z PDF:")
            preview_text = text[:4000] + ("..." if len(text) > 4000 else "")
            nice_box(preview_text.replace('\n', '<br>'))

        with tab2:
            if text.strip():
                # Najważniejsze informacje (punkty)
                with st.spinner("Ekstrakcja najważniejszych informacji..."):
                    key_points = extract_key_points_with_groq_api(text, st.session_state['api_key'])
                    st.header("Najważniejsze informacje")
                    key_points_md = "<br>".join(
                        f"- {line}" for line in [l.strip() for l in key_points.split('\n') if l.strip()]
                    )
                    nice_box(key_points_md)

                # Streszczenie ogólne
                with st.spinner("Generowanie streszczenia..."):
                    summary = summarize_briefly_with_groq_api(text, st.session_state['api_key'])
                    st.header("Streszczenie")
                    nice_box(summary.replace('\n', '<br>'))
            else:
                st.warning("Nie udało się wyciągnąć tekstu z PDF-a.")
else:
    if api_key and not st.session_state['api_key_loaded']:
        st.info("Wklej klucz i kliknij **Załaduj klucz**.")
    elif not api_key and key_loaded:
        st.warning("Wklej klucz przed kliknięciem 'Załaduj klucz'.")






