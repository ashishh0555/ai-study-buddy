import streamlit as st
import google.generativeai as genai
from datetime import datetime

# CONFIG API KEY AND MODEL
genai.configure(api_key="GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-2.5-flash")

from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

# SESSION STATE
if "history" not in st.session_state:
    st.session_state.history = []

if "total_words" not in st.session_state:
    st.session_state.total_words = 0

if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0

# PAGE
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Study Buddy")

# SIDEBAR
with st.sidebar:

    st.header("Statistics")

    st.metric(
        "Total Queries",
        st.session_state.total_queries
    )

    st.metric(
        "Total Words Generated",
        st.session_state.total_words
    )

    st.metric(
        "History Size",
        len(st.session_state.history)
    )

# INPUTS

style = st.radio(
    "Response Style",
    [
        "Beginner Friendly",
        "Professional"
    ]
)

if style == "Beginner Friendly":
    style_instruction = "Explain simply."
else:
    style_instruction = "Use professional terminology."

feature = st.selectbox(
    "Choose Feature",
    [
        "Explain Concept",
        "Summarize Text",
        "Generate Quiz Questions",
        "Translate Text"
    ]
)

language = st.selectbox(
    "Output Language",
    [
        "English",
        "Hindi",
        "Japanese",
        "French",
        "Kannada",
        "Telugu"
    ]
)

user_input = st.text_area(
    "Enter your text",
    height=200
)

# TRANSLATION OPTIONS

source_language = None
target_language = None

if feature == "Translate Text":

    col1, col2 = st.columns(2)

    with col1:
        source_language = st.text_input(
            "Source Language",
            value="English"
        )

    with col2:
        target_language = st.text_input(
            "Target Language",
            value="Hindi"
        )

# GENERATE BUTTON

if st.button("🚀 Generate Response"):

    if user_input.strip() == "":
        st.error("Please enter some text.")

    else:

        # PROMPTS

        if feature == "Explain Concept":

            prompt = f"""
Act as an expert educator.

Explain the following concept to a beginner:

{user_input}

Respond completely in {language}.
{style_instruction}

Requirements:
1. One sentence summary.
2. Real-world analogy.
3. Explain 2-3 key ideas.
4. Use bullet points.
5. Keep under 200 words.
"""

        elif feature == "Summarize Text":

            prompt = f"""
Provide a concise summary.

Text:
{user_input}

Respond completely in {language}.
{style_instruction}

Format:
- Executive Summary
- Key Takeaways
- Conclusion

Keep under 150 words.
"""

        elif feature == "Generate Quiz Questions":

            prompt = f"""
Generate exactly 5 engineering quiz questions on:

{user_input}

Respond completely in {language}.
{style_instruction}

For each question provide:
1. Scenario
2. Question
3. Correct Answer
4. Engineering Rationale
"""

        elif feature == "Translate Text":

            prompt = f"""
Translate the following text from
{source_language}
to
{target_language}

Text:

{user_input}

Preserve formatting and technical terminology.
"""

        # API CALL

        with st.spinner("Thinking..."):

            try:

                response = model.generate_content(prompt)

                response_text = response.text

            except Exception as e:

                st.error(f"Error: {e}")
                st.stop()

        # STATS

        word_count = len(response_text.split())

        st.session_state.total_words += word_count
        st.session_state.total_queries += 1

        current_time = datetime.now()

        st.session_state.history.append(
            {
                "time": current_time,
                "feature": feature,
                "input": user_input,
                "response": response_text
            }
        )

        # SAVE HISTORY

        with open(
            "history.txt",
            "a",
            encoding="utf-8"
        ) as file:

            file.write(
                f"\nFeature: {feature}\n"
            )

            file.write(
                f"Input: {user_input}\n"
            )

            file.write(
                f"Response: {response_text}\n"
            )

            file.write(
                f"Time: {current_time}\n"
            )

            file.write(
                "-" * 50 + "\n"
            )

        # DISPLAY RESPONSE

        st.success("Response Generated")

        st.markdown("### Response")

        st.markdown(response_text)

        st.metric(
            "Word Count",
            word_count
        )

        # DOWNLOAD BUTTON

        st.download_button(
            label="📥 Download Response",
            data=response_text,
            file_name="response.md",
            mime="text/markdown"
        )

# HISTORY

st.divider()

st.subheader("📜 Chat History")

if len(st.session_state.history) == 0:

    st.info("No history available.")

else:

    for item in reversed(st.session_state.history):

        with st.expander(
            f"{item['feature']} | {item['time'].strftime('%H:%M:%S')}"
        ):

            st.write(
                f"Input: {item['input']}"
            )

            st.write(
                item["response"]
            )