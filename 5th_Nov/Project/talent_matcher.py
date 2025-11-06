# app.py — Streamlit + LangChain Talent Matcher (Modern v0.2+, No Agent)

import streamlit as st
import pandas as pd
import json
import re
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

# Load environment variables from a .env file (recommended)
load_dotenv()

# === CONFIG ===
MODEL = "mistralai/mistral-7b-instruct"
MAX_PROFILES = 15
CSV_PATH = "employee_skills_dataset.csv"

# Page config
st.set_page_config(page_title="Talent Matcher", page_icon="👥", layout="wide")
st.title("👥 Talent Matcher")
st.markdown("Enter a PM request to find the **top 5 best-fitting employees** using AI ranking.")

# === SIDEBAR: API KEY & FILE UPLOAD ===
with st.sidebar:
    st.header("Configuration")
    api_key = os.getenv("OPENROUTER_API_KEY")
    uploaded_file = st.file_uploader("Upload employee_skills_dataset.csv", type=["csv"])

    if st.button("Clear Cache & Reload"):
        st.cache_data.clear()
        st.success("Cache cleared!")

# === LOAD DATA ===
@st.cache_data
def load_data(file):
    df = pd.read_csv(file).fillna("")
    return df

if uploaded_file:
    df = load_data(uploaded_file)
else:
    if os.path.exists(CSV_PATH):
        df = load_data(CSV_PATH)
    else:
        st.error(f"Please upload `{CSV_PATH}` or place it in the app directory.")
        st.stop()

st.success(f"Loaded **{len(df)} employees** from dataset.")

# === LLM SETUP ===
@st.cache_resource
def get_llm(_api_key):
    if not _api_key:
        st.warning("Please enter your OpenRouter API key.")
        st.stop()
    return ChatOpenAI(
        model=MODEL,
        openai_api_key=_api_key,
        openai_api_base="https://openrouter.ai/api/v1",
        temperature=0.1,
        max_tokens=1024
    )

llm = get_llm(api_key)

# === PROMPTS & CHAINS ===
extract_prompt = PromptTemplate.from_template("""
Summarize this request in 3 bullets:
• Role & seniority
• Skills + years
• Domain

Request: {query}

Bullets:
""")
extract_chain = extract_prompt | llm | StrOutputParser()

rank_prompt = PromptTemplate.from_template("""
PM Need:
{need}

All Candidates (JSON):
{profiles}

**TASK**: Return **ONLY** valid JSON array of **TOP 5** best matches.
Score 0-100. 2-sentence justification each.

Format exactly:
[
  {{"id": 101, "name": "Alice", "fit_score": 92, "justification": "Sentence 1. Sentence 2."}},
  ...
]

TOP 5 JSON ONLY. No other text.
""")
rank_chain = rank_prompt | llm | StrOutputParser()

# === CORE FUNCTIONS ===
def load_profiles(pm_need):
    profiles = []
    for _, row in df.head(MAX_PROFILES).iterrows():
        profiles.append({
            "id": int(row["ID"]),
            "name": row["Name"],
            "role": row["Role"],
            "seniority": row["Seniority"],
            "skills": row["Skills"],
            "years": int(row["Years_Experience"]) if pd.notna(row["Years_Experience"]) else 0,
            "domain": row["Last_Project_Domain"],
            "availability": int(row["Availability_Score"]) if pd.notna(row["Availability_Score"]) else 0,
            "bio": str(row["Bio"])[:500]
        })
    return json.dumps(profiles, ensure_ascii=False, indent=2)

def find_talent(query: str):
    if not query.strip():
        return None, "Please enter a valid request."

    with st.spinner("1. Extracting PM need..."):
        try:
            need = extract_chain.invoke({"query": query}).strip()
        except Exception as e:
            return None, f"Error extracting need: {e}"

    with st.spinner("2. Loading candidate profiles..."):
        profiles = load_profiles(need)

    with st.spinner("3. Ranking top 5 candidates..."):
        try:
            result = rank_chain.invoke({"need": need, "profiles": profiles})
        except Exception as e:
            return None, f"Error during ranking: {e}"

    # Parse JSON
    try:
        # 1. remove known noise
        for token in ["<s>", "[OUT]", "</s>"]:
            result = result.replace(token, "")
        # 2. extract the array
        match = re.search(r"\[.*\]", result, re.DOTALL)
        if not match:
            raise ValueError("No JSON array found")
        candidates = json.loads(match.group(0))
        return candidates, need
    except Exception as e:
        return None, (
            f"**JSON Parse Error:** {e}\n\n"
            f"**Raw output:**\n```json\n{result}\n```"
        )

# === MAIN UI ===
query = st.text_area(
    "PM Request",
    placeholder="e.g., Staff with Python skills in Fintech domain, at least 3 years experience",
    height=100
)

if st.button("Find Talent", type="primary"):
    if not api_key:
        st.error("Please enter your OpenRouter API key in the sidebar.")
    elif not query.strip():
        st.warning("Please enter a PM request.")
    else:
        candidates, info = find_talent(query)

        if candidates:
            # Show extracted need
            st.subheader("Extracted Need")
            st.code(info, language="text")

            # Show results
            st.subheader("Top 5 Matches")
            cols = st.columns(5)
            for i, c in enumerate(candidates[:5]):
                with cols[i]:
                    score = c.get("fit_score", 0)
                    color = "🟢" if score >= 80 else "🟡" if score >= 60 else "🔴"
                    st.metric(label=f"**{c['name']}**", value=f"{score}/100", delta=color)
                    with st.expander("Justification"):
                        st.write(c.get("justification", "No justification provided."))

            # Optional: Show raw JSON
            with st.expander("View Raw JSON Output"):
                st.json(candidates, expanded=False)
        else:
            st.error("Failed to get results.")
            st.markdown(info)

# === FOOTER ===
st.markdown("---")
st.caption("Powered by **LangChain** + **OpenRouter** (Mistral 7B) | Limited to first 15 profiles for speed.")