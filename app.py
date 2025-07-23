import streamlit as st
import PyPDF2
import requests

st.set_page_config(page_title="Agent PDF AI", page_icon="📄")
st.title("📄 Agent AI do ekstrakcji informacji z PDF (Groq API)")

# --- Cały blok instrukcji w jednej estetycznej ramce
def instruction_box():
    st.markdown(
        """
        <div style="
            border-radius: 18px;
            border: 2px solid #E0E7EF;
            background: #f7faff;
            padding: 1.5em 2em 1.1em 2em;
            margin-bottom: 2em;
            box-shadow: 0 3px 18px #0001;
            max-width: 570px;
        ">
            <b style="font-size: 1.10em;">Jak korzystać z aplikacji?</b>
            <ol style="margin-top: 1em; margin-bottom: 1.5em;">
                <li>Załóż darmowe konto lub zaloguj się na 
                    <a href="https://console.groq.com/keys" target="_blank" style="color:#2b68c4;"><b>Groq Platform</b></a>.
                </li>
                <li>
                    Wygeneruj nowy klucz (API Key):<br>
                    <div style="text-align:center;margin-top:0.6em;margin-bottom:0.6em;">
                        <img src="https://raw.githubusercontent.com/jcwigon/pdf_summarization_aiagent/main/Api%20groq.png" width="170" style="border-radius:10px;border:1px solid #eee;box-shadow:0 2px 8px #0001;">
                        <div style="font-size:0.97em;color:#7b8693;">Przycisk 'Create API Key' na Groq Platform</div>
                    </div>
                </li>
                <li>Wklej swój klucz API poniżej i kliknij <b>Załaduj klucz</b>.</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True
    )

instruction_box()







