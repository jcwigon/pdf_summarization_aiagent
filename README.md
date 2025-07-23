# Agent AI PDF – Streamlit App

Aplikacja do analizy dokumentów PDF z użyciem AI (OpenAI GPT) – wdrożona na Streamlit Cloud.

## Funkcje
- Wyciąganie tekstu z plików PDF
- Automatyczne streszczenie dokumentu przez GPT-3.5/4 (OpenAI)
- Prosty i nowoczesny interfejs (Streamlit)
- Wsparcie dla plików PDF z polskimi znakami

## Jak uruchomić aplikację lokalnie?
1. Zainstaluj wymagane biblioteki:
    ```
    pip install -r requirements.txt
    ```
2. Uruchom aplikację:
    ```
    streamlit run app.py
    ```
3. Wklej swój klucz OpenAI i wrzuć PDF – aplikacja pokaże tekst oraz streszczenie dokumentu.

## Deployment na Streamlit Cloud
1. Stwórz repozytorium na GitHub i wrzuć pliki: `app.py`, `requirements.txt`, `README.md`
2. Przejdź na [https://share.streamlit.io/](https://share.streamlit.io/) i połącz repozytorium
3. Aplikacja działa od razu online (do wprowadzenia własnego klucza OpenAI przez użytkownika)

## Autor
Jakub Ćwigoń  
2025