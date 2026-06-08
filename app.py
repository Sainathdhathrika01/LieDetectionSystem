import streamlit as st
import sounddevice as sd
import wavio
import numpy as np
import os

from auth import (
    register_user,
    login_user,
    save_prediction,
    get_user_history
)

from predict import predict_voice


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="AI Lie Detection System",
    layout="wide"
)

# CREATE AUDIO FOLDER
if not os.path.exists("audio_files"):
    os.makedirs("audio_files")


# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #001F3F, #003366, #00509E);
    color: white;
}

/* MAIN TITLE */
.main-title {
    text-align: center;
    font-size: 50px;
    font-weight: bold;
    color: #00BFFF;
    text-shadow: 2px 2px 10px black;
}

/* SUBTITLE */
.sub-title {
    text-align: center;
    font-size: 22px;
    color: #E0F7FF;
}

/* CARD DESIGN */
.card {
    background-color: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0px 0px 20px rgba(0,191,255,0.4);
    margin-top: 20px;
}

/* BUTTONS */
.stButton>button {
    background: linear-gradient(to right, #007BFF, #00BFFF);
    color: white;
    border-radius: 12px;
    height: 3em;
    font-size: 17px;
    font-weight: bold;
    border: none;
    width: 100%;
}

.stButton>button:hover {
    background: linear-gradient(to right, #0056D2, #0099FF);
    color: white;
    transform: scale(1.02);
}

/* METRICS */
[data-testid="metric-container"] {
    background-color: rgba(255,255,255,0.08);
    border: 1px solid #00BFFF;
    padding: 15px;
    border-radius: 15px;
    text-align: center;
}

/* AUDIO ICON */
.audio-img {
    display: block;
    margin-left: auto;
    margin-right: auto;
    width: 120px;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# SESSION VARIABLES
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "page" not in st.session_state:
    st.session_state.page = "home"

if "audio_path" not in st.session_state:
    st.session_state.audio_path = None

if "is_recording" not in st.session_state:
    st.session_state.is_recording = False

if "recording_data" not in st.session_state:
    st.session_state.recording_data = None


# -----------------------------
# HOME PAGE
# -----------------------------
st.markdown(
    '<h1 class="main-title">🎙️ AI Voice Lie Detection System</h1>',
    unsafe_allow_html=True
)

st.image(
    "https://cdn-icons-png.flaticon.com/512/3659/3659898.png",
    width=140
)

st.markdown(
    '<p class="sub-title">'
    'AI Voice Stress Analysis Using Machine Learning'
    '</p>',
    unsafe_allow_html=True
)

st.markdown("---")


# -----------------------------
# FEATURES CARD
# -----------------------------
st.markdown("""
<div class="card">

<h3>🔍 System Features</h3>

<ul>
<li>🎤 Voice Recording</li>
<li>🧠 AI Lie Detection</li>
<li>📊 Truth & Lie Scores</li>
<li>📜 User Prediction History</li>
<li>⚡ Fast Machine Learning Analysis</li>
</ul>

</div>
""", unsafe_allow_html=True)

st.markdown("---")


# -----------------------------
# TOP BUTTONS
# -----------------------------
col1, col2, col3 = st.columns([6, 1, 1])

with col2:
    if st.button("Register"):
        st.session_state.page = "register"

with col3:
    if st.button("Login"):
        st.session_state.page = "login"


# -----------------------------
# REGISTER PAGE
# -----------------------------
if (
    st.session_state.page == "register"
    and not st.session_state.logged_in
):

    st.subheader("📝 Create Account")

    new_user = st.text_input(
        "Username",
        key="register_user"
    )

    new_pass = st.text_input(
        "Password",
        type="password",
        key="register_pass"
    )

    if st.button("Submit Registration"):

        try:

            register_user(new_user, new_pass)

            st.success("✅ Registration Successful")

        except:

            st.error("❌ Username already exists")


# -----------------------------
# LOGIN PAGE
# -----------------------------
if (
    st.session_state.page == "login"
    and not st.session_state.logged_in
):

    st.subheader("🔐 Login")

    username = st.text_input(
        "Enter Username",
        key="login_user"
    )

    password = st.text_input(
        "Enter Password",
        type="password",
        key="login_pass"
    )

    if st.button("Submit Login"):

        user = login_user(username, password)

        if user:

            st.session_state.logged_in = True
            st.session_state.username = username

            st.success("✅ Login Successful")

            st.rerun()

        else:

            st.error("❌ Invalid Username or Password")


# -----------------------------
# DASHBOARD
# -----------------------------
if st.session_state.logged_in:

    st.markdown("---")

    st.header(
        f"👋 Welcome {st.session_state.username}"
    )

    st.image(
        "https://cdn-icons-png.flaticon.com/512/727/727245.png",
        width=100
    )

    st.subheader("🎤 Voice Recording")

    fs = 44100
    duration = 10


    # -----------------------------
    # START RECORDING
    # -----------------------------
    if not st.session_state.is_recording:

        if st.button("🎙️ Start Recording"):

            st.session_state.is_recording = True

            st.warning("🔴 Recording Started... Speak Now")

            st.session_state.recording_data = sd.rec(
                int(duration * fs),
                samplerate=fs,
                channels=1,
                dtype='int16'
            )

            st.rerun()


    # -----------------------------
    # STOP RECORDING
    # -----------------------------
    else:

        st.warning("🔴 Recording in Progress...")

        if st.button("⏹️ Stop Recording"):

            sd.wait()

            audio_path = (
                f"audio_files/"
                f"{st.session_state.username}.wav"
            )

            wavio.write(
                audio_path,
                st.session_state.recording_data,
                fs,
                sampwidth=2
            )

            st.session_state.audio_path = audio_path

            st.session_state.is_recording = False

            st.success("✅ Recording Saved")

            st.rerun()


    # -----------------------------
    # AUDIO PLAYER
    # -----------------------------
    if st.session_state.audio_path:

        st.markdown("---")

        st.audio(st.session_state.audio_path)

        st.markdown("---")


        # -----------------------------
        # ANALYZE BUTTON
        # -----------------------------
        if st.button("🧠 Analyze Voice"):

            with st.spinner("Analyzing Voice..."):

                prediction, scores = predict_voice(
                    st.session_state.audio_path
                )

                truth_score = float(
                    scores.get("Truth", 0)
                )

                lie_score = float(
                    scores.get("Lie", 0)
                )

                # FIXED LOGIC
                if truth_score >= lie_score:

                    prediction = "Truth"

                    accuracy = truth_score

                else:

                    prediction = "Lie"

                    accuracy = lie_score


                # RESULT
                if prediction == "Truth":

                    result_text = "✅ TRUTH"

                    summary = """
                    • Voice stress appears low

                    • Speech pattern stable

                    • Emotional fluctuation minimal

                    • Classified as truthful speech
                    """

                else:

                    result_text = "❌ LIE"

                    summary = """
                    • Stress patterns detected

                    • Voice fluctuation higher

                    • Emotional instability observed

                    • Classified as deceptive speech
                    """


                # SAVE RESULT
                save_prediction(
                    st.session_state.username,
                    prediction,
                    truth_score,
                    lie_score,
                    accuracy,
                    st.session_state.audio_path
                )

            st.markdown("---")

            # -----------------------------
            # METRICS
            # -----------------------------
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Truth Score",
                    f"{truth_score:.2f}%"
                )

            with col2:
                st.metric(
                    "Lie Score",
                    f"{lie_score:.2f}%"
                )

            with col3:
                st.metric(
                    "Accuracy",
                    f"{accuracy:.2f}%"
                )

            st.markdown("---")


            # -----------------------------
            # FINAL PREDICTION
            # -----------------------------
            st.subheader("📌 Final Prediction")

            if prediction == "Truth":

                st.success(result_text)

            else:

                st.error(result_text)

            st.markdown("---")


            # -----------------------------
            # SUMMARY
            # -----------------------------
            st.subheader("📄 Prediction Summary")

            st.write(summary)

            st.markdown("---")


            # -----------------------------
            # TECHNICAL REPORT
            # -----------------------------
            st.subheader("⚙️ Technical Report")

            st.write("""
            • Voice recorded successfully

            • MFCC features extracted

            • SVM classification completed

            • Confidence analysis generated
            """)


    # -----------------------------
    # HISTORY
    # -----------------------------
    st.markdown("---")

    st.subheader("📜 User Prediction History")

    history = get_user_history(
        st.session_state.username
    )

    if history:

        for row in history:

            st.info(f'''
Result: {row[0]}

Truth Score: {row[1]}%

Lie Score: {row[2]}%

Accuracy: {row[3]}%

Date: {row[4]}
''')

    else:

        st.warning("No History Available")


    # -----------------------------
    # LOGOUT
    # -----------------------------
    st.markdown("---")

    if st.button("🚪 Logout"):

        st.session_state.logged_in = False

        st.session_state.username = ""

        st.session_state.audio_path = None

        st.success("Logged Out Successfully")

        st.rerun()