import os
import requests
import streamlit as st

from rag_app.rag_chain import ask_rag

#API_URL = "http://127.0.0.1:8000/query"
#API_URL = "http://api:8000/query"

APP_MODE = os.getenv("APP_MODE", "direct") # "direct" or "api"
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/query")

st.set_page_config(page_title="AI Policy RAG Assistant", page_icon="🤖", layout="wide")

st.title("AI Policy RAG Assistant")
st.write("Ask questions about the EU AI Act, GDPR, and NIST AI Risk Management Framework.")

question = st.text_area(
    "Your question", 
    placeholder="Example: What are high-risk AI systems under the EU AI Act?")

source_option = st.selectbox(
    "Choose source",
    [
        "Auto detect",
        "EU AI Act",
        "GDPR",
        "NIST AI RMF",
    ],
)

source_map = {
    "Auto detect": None,
    "EU AI Act": "eu_ai_act.pdf",
    "GDPR": "gdpr.pdf",
    "NIST AI RMF": "nist_ai_rmf.pdf",
}

k = st.slider("Number of retrieved chunks", min_value=3, max_value=15, value=6)

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        payload = {
            "question": question,
            "k": k,
            "source_filter": source_map[source_option],
        }
        with st.spinner("Retrieving documents and generating answer..."):
            if APP_MODE == "api":
                response = requests.post(API_URL, json=payload, timeout=120)

                if response.status_code != 200:
                    st.error(f"API error: {response.status_code}")
                    st.text(response.text)
                    st.stop()
                result = response.json()
            
            else:                
                result = ask_rag(
                    question=payload["question"],
                    k=payload["k"],
                    source_filter=payload["source_filter"],
                )
        st.subheader("Answer")
        st.write(result["answer"])

        st.subheader("Sources")
        if result["sources"]:
            for i, source in enumerate(result["sources"], start=1):
                st.markdown(
                    f"**{i}. {source['source']} — page {source['page']}**"
                )
                st.caption(source["preview"])
        else:
            st.info("No sources returned.")
        # else:
        #     st.error(f"API error: {response.status_code}")
        #     st.text(response.text)