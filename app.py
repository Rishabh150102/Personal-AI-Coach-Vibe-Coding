import os
from html import escape
from typing import List

import streamlit as st
from openai import APIConnectionError, APIStatusError, AuthenticationError, OpenAI, RateLimitError
from dotenv import load_dotenv
load_dotenv()

from prompts import PERSONA_OPTIONS, SYSTEM_PROMPT_TEMPLATE, USER_PROMPT_TEMPLATE


MEMORY_WINDOW = 6
LANGUAGE_OPTIONS = [
    "English",
    "Hindi",
    "Spanish",
    "French",
    "German",
    "Portuguese",
    "Japanese",
]


def init_session_state() -> None:
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "translations" not in st.session_state:
        st.session_state.translations = {}


def normalize_message(role: str, content: str) -> str:
    normalized_content = content.strip()
    if role == "user":
        prefixes = ["user request:", "you:"]
        for prefix in prefixes:
            if normalized_content.lower().startswith(prefix):
                normalized_content = normalized_content.split(":", 1)[1].strip()
        normalized_content = normalized_content.replace('<div class="chat-content">', "")
        normalized_content = normalized_content.replace("</div>", "")
    return normalized_content.strip()


def render_message(role: str, content: str) -> None:
    bubble_class = "user-bubble" if role == "user" else "assistant-bubble"
    wrapper_class = "user-row" if role == "user" else "assistant-row"
    normalized_content = normalize_message(role, content)
    content_html = escape(normalized_content).replace("\n", "<br>")
    st.markdown(
        f"""
        <div class="chat-row {wrapper_class}">
            <div class="chat-bubble {bubble_class}">
                <div class="chat-content">{content_html}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_messages(
    persona_key: str,
    user_input: str,
    warmth: str,
    directness: str,
    response_length: str,
    focus_area: str,
    memory_enabled: bool,
) -> List[dict]:
    persona = PERSONA_OPTIONS[persona_key]
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(
        persona_name=persona["label"],
        persona_description=persona["description"],
    )
    style_settings = f"""

Additional personality settings:
- Warmth level: {warmth}
- Directness level: {directness}
- Response length: {response_length}
- Focus area: {focus_area}

Follow these settings closely while staying consistent with the selected persona.
"""
    user_prompt = USER_PROMPT_TEMPLATE.format(user_input=user_input.strip())
    messages = [
        {"role": "system", "content": f"{system_prompt}{style_settings}"},
    ]
    if memory_enabled:
        messages.extend(st.session_state.conversation_history[-MEMORY_WINDOW:])
    messages.append({"role": "user", "content": user_prompt})
    return messages


def get_client() -> OpenAI:
    api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")
    return OpenAI(api_key=api_key)


def format_request_error(exc: Exception) -> str:
    if isinstance(exc, APIConnectionError):
        cause = getattr(exc, "__cause__", None)
        details = f" Details: {cause}" if cause else ""
        return (
            "Could not reach the OpenAI API. Check your internet connection, VPN, firewall, "
            f"or proxy settings, then try again.{details}"
        )

    if isinstance(exc, AuthenticationError):
        return "Authentication failed. Check whether OPENAI_API_KEY is set correctly for this terminal session."

    if isinstance(exc, RateLimitError):
        return "The request was rate limited. Wait a moment and try again."

    if isinstance(exc, APIStatusError):
        status_code = getattr(exc, "status_code", "unknown")
        return f"OpenAI API returned an error (HTTP {status_code}). {exc}"

    return str(exc)


def translate_response(text: str, target_language: str, model: str) -> str:
    if target_language == "English":
        return text

    client = get_client()
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": (
                    "Translate the assistant response into the requested language. "
                    "Preserve meaning, tone, structure, and bullet points. "
                    "Return only the translated text."
                ),
            },
            {
                "role": "user",
                "content": f"Target language: {target_language}\n\nText:\n{text}",
            },
        ],
    )
    return response.output_text.strip()


def get_display_content(role: str, content: str, output_language: str, model: str) -> str:
    normalized_content = normalize_message(role, content)
    if role != "assistant" or output_language == "English":
        return normalized_content

    cache_key = (normalized_content, output_language, model)
    if cache_key not in st.session_state.translations:
        with st.spinner(f"Translating to {output_language}..."):
            st.session_state.translations[cache_key] = translate_response(
                normalized_content,
                output_language,
                model,
            )
    return st.session_state.translations[cache_key]


def generate_response(
    persona_key: str,
    user_input: str,
    model: str,
    warmth: str,
    directness: str,
    response_length: str,
    focus_area: str,
    memory_enabled: bool,
) -> str:
    client = get_client()
    messages = build_messages(
        persona_key,
        user_input,
        warmth,
        directness,
        response_length,
        focus_area,
        memory_enabled,
    )
    response = client.responses.create(model=model, input=messages)
    return response.output_text.strip()


st.set_page_config(page_title="Personal AI Coach", page_icon=":speech_balloon:", layout="wide")
init_session_state()
st.markdown(
    """
    <style>
    .block-container {
        max-width: 1440px;
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }
    .chat-row {
        display: flex;
        margin: 0.65rem 0;
    }
    .assistant-row {
        justify-content: flex-start;
    }
    .user-row {
        justify-content: flex-end;
    }
    .chat-bubble {
        max-width: 78%;
        padding: 0.9rem 1rem;
        border-radius: 16px;
        line-height: 1.5;
    }
    .assistant-bubble {
        background: linear-gradient(135deg, #1f2937, #111827);
        border: 1px solid #374151;
    }
    .user-bubble {
        background: linear-gradient(135deg, #153b2e, #0f2c22);
        border: 1px solid #2f6a56;
    }
    .chat-content {
        margin: 0;
        font-size: 1rem;
    }
    .app-title {
        text-align: center;
        margin-bottom: 0.25rem;
    }
    .app-subtitle {
        text-align: center;
        color: #9ca3af;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<h1 class="app-title">Personal AI Coach</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="app-subtitle">Get personalized coaching advice on any topic, powered by the OpenAI API. Adjust the settings in the sidebar to customize the coaching style and response.</p>',
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Settings")
    persona_key = st.selectbox("Persona", options=list(PERSONA_OPTIONS.keys()), format_func=lambda key: PERSONA_OPTIONS[key]["label"])
    st.caption(PERSONA_OPTIONS[persona_key]["description"].splitlines()[0].replace("Tone: ", ""))
    warmth = st.select_slider("Warmth", options=["Low", "Medium", "High"], value="Medium")
    directness = st.select_slider("Directness", options=["Low", "Medium", "High"], value="Medium")
    response_length = st.selectbox("Response Length", options=["Brief", "Balanced", "Detailed"], index=1)
    focus_area = st.selectbox(
        "Coaching Focus",
        options=["Motivation", "Clarity", "Action Plan", "Accountability", "Confidence"],
        index=2,
    )
    output_language = st.selectbox("Response Language", options=LANGUAGE_OPTIONS, index=0)
    memory_enabled = st.toggle("Session Memory", value=True)
    if st.button("Clear Memory"):
        st.session_state.conversation_history = []
        st.session_state.chat_history = []
        st.success("Session memory cleared.")
    model = st.text_input("Model", value="gpt-4o-mini")
    st.markdown("Set `OPENAI_API_KEY` in your environment before running the app.")

for message in st.session_state.chat_history[-MEMORY_WINDOW:]:
    render_message(
        message["role"],
        get_display_content(message["role"], message["content"], output_language, model),
    )

with st.form("coach_prompt_form", clear_on_submit=True):
    user_input = st.text_area(
        "What would you like coaching on?",
        height=180,
        placeholder="I keep procrastinating on important work. Help me make a plan.",
    )
    submitted = st.form_submit_button("Get Coaching Advice", type="primary")

if submitted:
    if not user_input.strip():
        st.warning("Enter a message first.")
    else:
        try:
            with st.spinner("Thinking..."):
                answer = generate_response(
                    persona_key,
                    user_input,
                    model,
                    warmth,
                    directness,
                    response_length,
                    focus_area,
                    memory_enabled,
                )
            st.session_state.chat_history.extend(
                [
                    {"role": "user", "content": user_input.strip()},
                    {"role": "assistant", "content": answer},
                ]
            )
            if memory_enabled:
                st.session_state.conversation_history.extend(
                    [
                        {"role": "user", "content": user_input.strip()},
                        {"role": "assistant", "content": answer},
                    ]
                )
            st.rerun()
        except Exception as exc:
            st.error(f"Request failed: {format_request_error(exc)}")
