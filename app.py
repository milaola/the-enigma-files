
import streamlit as st

st.set_page_config(
    page_title="The Enigma Files | Classified",
    page_icon="🗝️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- PAGE STYLING ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Cinzel:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');

.stApp {
    background:
        radial-gradient(ellipse at top, #241719 0%, #101014 48%, #08090c 100%);
    color: #e8e2d8;
}

header[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

h1, h2, h3 {
    font-family: 'Cinzel', serif !important;
}

.terminal {
    font-family: 'Share Tech Mono', monospace;
    color: #b99b65;
    letter-spacing: 3px;
    font-size: 12px;
}

.hero {
    text-align: center;
    padding: 65px 20px 45px 20px;
    border-top: 1px solid #59432f;
    border-bottom: 1px solid #59432f;
    background: linear-gradient(180deg, #1d1518aa, #10101422);
    margin: 20px 0 35px 0;
}

.hero h1 {
    font-size: clamp(35px, 6vw, 65px);
    letter-spacing: 7px;
    color: #e5d2ae;
    margin-bottom: 10px;
}

.hero p {
    color: #a69a8c;
    letter-spacing: 3px;
    font-family: 'Share Tech Mono', monospace;
}

.warning {
    border: 1px solid #713c37;
    background: #271719;
    padding: 15px 20px;
    color: #d7aaa0;
    font-family: 'Share Tech Mono', monospace;
    font-size: 13px;
    margin: 25px 0;
}

.room {
    background: linear-gradient(145deg, #1b1b20, #111115);
    border: 1px solid #51412f;
    padding: 25px;
    min-height: 245px;
    border-radius: 5px;
    transition: 0.3s ease;
}

.room:hover {
    border-color: #b99b65;
    transform: translateY(-4px);
}

.room-number {
    font-family: 'Share Tech Mono', monospace;
    color: #a88b5d;
    font-size: 12px;
    letter-spacing: 2px;
}

.room h3 {
    color: #e5d2ae;
    font-size: 21px;
    margin-top: 15px;
}

.room p {
    color: #aaa19a;
    font-size: 14px;
    line-height: 1.7;
}

.stButton > button {
    background: #6c2928;
    color: #f2e8d9;
    border: 1px solid #a76d55;
    border-radius: 2px;
    padding: 10px 25px;
    font-family: 'Share Tech Mono', monospace;
    letter-spacing: 2px;
    transition: 0.3s;
}

.stButton > button:hover {
    background: #923d36;
    border-color: #d1ad78;
    color: white;
}

hr {
    border-color: #42372e;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------

if "selected_room" not in st.session_state:
    st.session_state.selected_room = None

if "started" not in st.session_state:
    st.session_state.started = False


# ---------------- HEADER ----------------

st.markdown("""
<div class="terminal">
    SYSTEM ID: EF-001 &nbsp; | &nbsp; SECURITY LEVEL: RESTRICTED
    &nbsp; | &nbsp; ACCESS: PENDING
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="terminal">CLASSIFIED INVESTIGATION DIVISION</div>
    <h1>THE ENIGMA FILES</h1>
    <p>THREE ROOMS. THREE CHALLENGES. ONE WAY OUT.</p>
    <div class="terminal">[ YOUR MISSION BEGINS HERE ]</div>
</div>
""", unsafe_allow_html=True)


# ---------------- WARNING ----------------

st.markdown("""
<div class="warning">
    ⚠ SECURITY NOTICE: UNAUTHORISED ACCESS DETECTED.<br>
    The facility has been placed under lockdown.
    Complete all three challenges to initiate the exit sequence.
</div>
""", unsafe_allow_html=True)


# ---------------- INTRODUCTION ----------------

st.markdown("## THE MISSION")

st.write("""
You have regained consciousness inside an abandoned research facility.
The doors are sealed. The security system is active, and an unknown
operator is monitoring your movements.

Three encrypted rooms stand between you and freedom.

Your only way out is to solve what lies within them.
""")

st.divider()

# ---------------- ROOM CARDS ----------------

st.markdown("## CLASSIFIED ROOM DIRECTORY")

st.caption("SELECT A ROOM TO REVIEW ITS MISSION BRIEFING.")

col1, col2, col3 = st.columns(3)

rooms = [
    {
        "number": "01 / LEVEL ONE",
        "name": "THE CODE VAULT",
        "description": "A numerical sequence guards the first security checkpoint. Find the missing pattern to recover the access code.",
        "difficulty": "DIFFICULTY: RECONNAISSANCE",
        "key": "room1"
    },
    {
        "number": "02 / LEVEL TWO",
        "name": "THE HIDDEN MESSAGE",
        "description": "An encrypted message has been intercepted. Decode the scrambled information to uncover the password.",
        "difficulty": "DIFFICULTY: DECRYPTION",
        "key": "room2"
    },
    {
        "number": "03 / LEVEL THREE",
        "name": "THE FINAL CHALLENGE",
        "description": "A collection of clues conceals the final answer. Your reasoning will determine whether you escape.",
        "difficulty": "DIFFICULTY: CRITICAL",
        "key": "room3"
    }
]

for col, room in zip([col1, col2, col3], rooms):
    with col:
        st.markdown(f"""
        <div class="room">
            <div class="room-number">{room['number']}</div>
            <h3>{room['name']}</h3>
            <p>{room['description']}</p>
            <div class="terminal">{room['difficulty']}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("ACCESS ROOM", key=room["key"], use_container_width=True):
            st.session_state.selected_room = room["key"]
            st.session_state.started = True

# ---------------- SELECTED ROOM ----------------

if st.session_state.selected_room:
    selected = st.session_state.selected_room

    st.divider()

    room_details = {
        "room1": ("THE CODE VAULT", "Your first objective is to identify the missing number in a sequence. A correct answer will reveal the security code."),
        "room2": ("THE HIDDEN MESSAGE", "A coded message awaits. Identify the encryption pattern and recover the hidden password."),
        "room3": ("THE FINAL CHALLENGE", "Examine the evidence, connect the clues and identify the correct solution to unlock the exit.")
    }

    name, briefing = room_details[selected]

    st.markdown(f"### MISSION BRIEFING: {name}")
    st.write(briefing)

    st.info("Room interface selected. Puzzle mechanics will be connected to this screen in the next development stage.")

    if st.button("RETURN TO DIRECTORY"):
        st.session_state.selected_room = None
        st.rerun()


# ---------------- FOOTER ----------------

st.divider()

st.markdown("""
<div style="text-align:center; padding:20px;">
    <div class="terminal">THE ENIGMA FILES // CLASSIFIED ARCHIVES</div>
    <p style="color:#70675e; font-size:12px;">
        THINK CAREFULLY. EVERY CLUE MATTERS.
    </p>
</div>
""", unsafe_allow_html=True)
