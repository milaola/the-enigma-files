
import html
import streamlit as st

from database import (
    create_player,
    complete_room,
    record_attempt,
    record_hint,
    get_player_progress,
    get_leaderboard,
    get_player_by_id
)

from puzzles.code_vault import (
    SEQUENCE,
    SECURITY_CODE,
    HINTS,
    check_answer
)

from puzzles.hidden_message import (
    ENCRYPTED_MESSAGE,
    SECURITY_PASSWORD,
    HINTS as MESSAGE_HINTS,
    check_answer as check_message_answer
)

from puzzles.final_challenge import (
    SECURITY_PHRASE,
    HINTS as FINAL_HINTS,
    check_answer as check_final_answer
)


# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="The Enigma Files | Classified",
    page_icon="🗝️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ---------------- SESSION STATE INITIALIZATION ----------------

defaults = {
    "player_name": "",
    "player_id": None,
    "player_access_id": None,
    "selected_room": None,
    "started": False,
    "progress_loaded": False,

    "room1_completed": False,
    "room1_attempts": 0,
    "room1_hint_level": 0,

    "room2_completed": False,
    "room2_attempts": 0,
    "room2_hint_level": 0,

    "room3_completed": False,
    "room3_attempts": 0,
    "room3_hint_level": 0,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------- HELPER FUNCTIONS ----------------

def load_progress():
    """Load saved player progress from the database."""

    if st.session_state.progress_loaded:
        return

    progress = get_player_progress(
        st.session_state.player_id
    )

    for room_number, room_data in progress.items():

        st.session_state[f"room{room_number}_completed"] = (
            room_data["completed"]
        )

        st.session_state[f"room{room_number}_attempts"] = (
            room_data["attempts"]
        )

        st.session_state[f"room{room_number}_hint_level"] = (
            room_data["hints_used"]
        )

    st.session_state.progress_loaded = True


def finish_room(room_number):
    """Save room completion and award points only once."""

    completed_key = f"room{room_number}_completed"

    if not st.session_state[completed_key]:

        complete_room(
            st.session_state.player_id,
            room_number,
            points=100
        )

        st.session_state[completed_key] = True


def room_is_unlocked(room_number):
    """Check whether a player has unlocked a room."""

    if room_number == 1:
        return True

    if room_number == 2:
        return st.session_state.room1_completed

    if room_number == 3:
        return st.session_state.room2_completed

    return False


def show_hint(button_label, hint_list, room_number):
    """Display and save the player's hint usage."""

    hint_key = f"room{room_number}_hint_level"

    if st.button(
        button_label,
        key=f"hint_button_{room_number}"
    ):

        if st.session_state[hint_key] < len(hint_list):

            record_hint(
                st.session_state.player_id,
                room_number
            )

            st.session_state[hint_key] += 1

    if st.session_state[hint_key] > 0:

        hint = hint_list[
            st.session_state[hint_key] - 1
        ]

        st.info(f"INTELLIGENCE REPORT: {hint}")

    if st.session_state[hint_key] >= len(hint_list):
        st.caption("ALL AVAILABLE HINTS HAVE BEEN REVEALED.")


def record_failed_attempt(room_number):
    """Save an unsuccessful answer."""

    attempts_key = f"room{room_number}_attempts"

    st.session_state[attempts_key] += 1

    record_attempt(
        st.session_state.player_id,
        room_number
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


# ---------------- PLAYER REGISTRATION AND LOGIN ----------------

if not st.session_state.started:

    st.markdown("## IDENTIFY YOURSELF")

    auth_mode = st.radio(
        "SELECT ACCESS TYPE",
        ["NEW AGENT", "RETURNING AGENT"],
        horizontal=True
    )

    # NEW PLAYER REGISTRATION

    if auth_mode == "NEW AGENT":

        st.write(
            "Register a new identity to begin the investigation."
        )

        with st.form("player_registration_form"):

            player_name = st.text_input(
                "PLAYER NAME",
                placeholder="Enter your name..."
            )

            submitted = st.form_submit_button(
                "REGISTER AND START"
            )

            if submitted:

                if not player_name.strip():

                    st.error("Please enter your name.")

                else:

                    clean_name = player_name.strip()

                    player_id = create_player(clean_name)

                    st.session_state.player_id = player_id
                    st.session_state.player_name = clean_name
                    st.session_state.player_access_id = player_id
                    st.session_state.started = True
                    st.session_state.progress_loaded = False

                    st.rerun()

    # RETURNING PLAYER LOGIN

    else:

        st.write(
            "Enter your registered details to resume your investigation."
        )

        with st.form("player_login_form"):

            access_id = st.number_input(
                "PLAYER ID",
                min_value=1,
                step=1
            )

            player_name = st.text_input(
                "PLAYER NAME",
                placeholder="Enter your registered name..."
            )

            submitted = st.form_submit_button(
                "RESUME INVESTIGATION"
            )

            if submitted:

                if not player_name.strip():

                    st.error("Please enter your name.")

                else:

                    player = get_player_by_id(
                        int(access_id),
                        player_name
                    )

                    if player is None:

                        st.error(
                            "IDENTITY NOT FOUND. "
                            "CHECK YOUR PLAYER ID AND NAME."
                        )

                    else:

                        st.session_state.player_id = player[0]
                        st.session_state.player_name = player[1]
                        st.session_state.player_access_id = player[0]
                        st.session_state.started = True
                        st.session_state.progress_loaded = False

                        st.rerun()

    st.stop()


# ---------------- LOAD SAVED PROGRESS ----------------

load_progress()


# ---------------- PLAYER INFORMATION ----------------

st.markdown(
    f"**AGENT:** {html.escape(st.session_state.player_name)}"
)

st.info(
    f"YOUR PLAYER ID: {st.session_state.player_access_id} "
    "| Keep this ID to access your saved progress later."
)

completed_rooms = sum([
    st.session_state.room1_completed,
    st.session_state.room2_completed,
    st.session_state.room3_completed
])

st.caption(f"ROOMS COMPLETED: {completed_rooms}/3")

if completed_rooms == 3:

    st.success(
        "ALL SECURITY CHECKPOINTS OVERRIDDEN. YOU HAVE ESCAPED!"
    )


# ---------------- ROOM DIRECTORY ----------------

st.markdown("## CLASSIFIED ROOM DIRECTORY")

st.caption(
    "SELECT AN UNLOCKED ROOM TO BEGIN OR CONTINUE YOUR INVESTIGATION."
)

rooms = [
    {
        "number": "01 / LEVEL ONE",
        "name": "THE CODE VAULT",
        "description": "A numerical sequence guards the first security checkpoint. Find the missing pattern to recover the access code.",
        "difficulty": "DIFFICULTY: RECONNAISSANCE",
        "key": "room1",
        "room_number": 1
    },
    {
        "number": "02 / LEVEL TWO",
        "name": "THE HIDDEN MESSAGE",
        "description": "An encrypted message has been intercepted. Decode the scrambled information to uncover the password.",
        "difficulty": "DIFFICULTY: DECRYPTION",
        "key": "room2",
        "room_number": 2
    },
    {
        "number": "03 / LEVEL THREE",
        "name": "THE FINAL CHALLENGE",
        "description": "A collection of clues conceals the final answer. Your reasoning will determine whether you escape.",
        "difficulty": "DIFFICULTY: CRITICAL",
        "key": "room3",
        "room_number": 3
    }
]

columns = st.columns(3)

for col, room in zip(columns, rooms):

    room_number = room["room_number"]

    unlocked = room_is_unlocked(room_number)

    completed = st.session_state[
        f"room{room_number}_completed"
    ]

    with col:

        st.markdown(f"""
        <div class="room">
            <div class="room-number">{room['number']}</div>
            <h3>{room['name']}</h3>
            <p>{room['description']}</p>
            <div class="terminal">{room['difficulty']}</div>
        </div>
        """, unsafe_allow_html=True)

        if completed:

            st.success("COMPLETED")

        elif not unlocked:

            st.warning("LOCKED")

        else:

            st.info("AVAILABLE")

        if st.button(
            "ACCESS ROOM",
            key=room["key"],
            use_container_width=True,
            disabled=not unlocked
        ):

            st.session_state.selected_room = room["key"]
            st.rerun()


# ---------------- ROOM 1: THE CODE VAULT ----------------

if st.session_state.selected_room == "room1":

    st.divider()

    st.markdown(
        '<div class="terminal">ACCESSING FILE: EF-001-A</div>',
        unsafe_allow_html=True
    )

    st.markdown("# THE CODE VAULT")

    st.warning(
        "SECURITY LOCK ACTIVE. IDENTIFY THE MISSING NUMBER "
        "TO RETRIEVE THE ACCESS CODE."
    )

    st.write("""
    An encrypted security system protects the first room.

    A sequence of numbers has been recovered from the facility's
    mainframe. One number is missing.

    Identify the pattern and enter the missing number.
    """)

    st.markdown("### RECOVERED DATA")

    sequence_display = "   →   ".join(
        str(number) for number in SEQUENCE
    )

    st.markdown(
        f"""
        <div style="
            background:#17171d;
            border:1px solid #8c7049;
            padding:25px;
            text-align:center;
            font-size:25px;
            color:#d6b77d;
            font-family:monospace;
            letter-spacing:3px;
        ">
            {html.escape(sequence_display)}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    if not st.session_state.room1_completed:

        with st.form("code_vault_form"):

            user_answer = st.text_input(
                "ENTER THE MISSING NUMBER",
                placeholder="Awaiting input..."
            )

            submitted = st.form_submit_button(
                "SUBMIT ANSWER",
                use_container_width=True
            )

            if submitted:

                if check_answer(user_answer):

                    finish_room(1)
                    st.rerun()

                else:

                    record_failed_attempt(1)

                    st.error(
                        "ACCESS DENIED. THE SEQUENCE DOES NOT MATCH."
                    )

        st.divider()

        st.markdown("### INVESTIGATION NOTES")

        show_hint("REQUEST HINT", HINTS, 1)

        st.caption(
            f"ATTEMPTS: {st.session_state.room1_attempts}"
        )

    else:

        st.success(
            "ACCESS GRANTED. SECURITY SYSTEM OVERRIDDEN."
        )

        st.markdown("## SECURITY CODE RECOVERED")

        st.markdown(
            f"""
            <div style="
                background:#17171d;
                border:1px solid #b99b65;
                padding:30px;
                text-align:center;
            ">
                <div style="
                    color:#b99b65;
                    font-family:monospace;
                    letter-spacing:4px;
                ">
                    RECOVERED SECURITY CODE
                </div>
                <div style="
                    color:#f0d8a8;
                    font-size:48px;
                    letter-spacing:12px;
                    font-family:monospace;
                ">
                    {html.escape(str(SECURITY_CODE))}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write(
            "The first security checkpoint has been successfully bypassed."
        )

        st.info("ROOM 2 IS NOW UNLOCKED.")


# ---------------- ROOM 2: THE HIDDEN MESSAGE ----------------

elif st.session_state.selected_room == "room2":

    st.divider()

    st.markdown(
        '<div class="terminal">ACCESSING FILE: EF-002-B</div>',
        unsafe_allow_html=True
    )

    st.markdown("# THE HIDDEN MESSAGE")

    st.warning(
        "INTERCEPTED TRANSMISSION DETECTED. DECRYPTION REQUIRED."
    )

    st.write("""
    An unknown operator has left an encrypted message
    inside the facility's communication system.

    The message contains the password needed to access
    the next security checkpoint.

    Recover the original message before the transmission
    is permanently deleted.
    """)

    st.markdown("### INTERCEPTED TRANSMISSION")

    st.markdown(
        f"""
        <div style="
            background:#17171d;
            border:1px solid #8c7049;
            padding:30px;
            text-align:center;
        ">
            <div style="
                color:#b99b65;
                font-family:monospace;
                letter-spacing:3px;
                font-size:12px;
            ">
                ENCRYPTED DATA
            </div>
            <div style="
                color:#e5d2ae;
                font-size:42px;
                letter-spacing:12px;
                font-family:monospace;
                padding:15px;
            ">
                {html.escape(str(ENCRYPTED_MESSAGE))}
            </div>
            <div style="
                color:#8d7771;
                font-family:monospace;
                font-size:11px;
            ">
                ENCRYPTION TYPE: CAESAR CIPHER
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.markdown("### DECRYPTION TERMINAL")

    if not st.session_state.room2_completed:

        with st.form("hidden_message_form"):

            user_message = st.text_input(
                "ENTER THE DECRYPTED WORD",
                placeholder="Awaiting decoded message..."
            )

            submitted = st.form_submit_button(
                "DECRYPT MESSAGE",
                use_container_width=True
            )

            if submitted:

                if check_message_answer(user_message):

                    finish_room(2)
                    st.rerun()

                else:

                    record_failed_attempt(2)

                    st.error(
                        "DECRYPTION FAILED. MESSAGE DOES NOT MATCH."
                    )

        st.divider()

        st.markdown("### CLASSIFIED INTELLIGENCE")

        show_hint(
            "REQUEST INTELLIGENCE REPORT",
            MESSAGE_HINTS,
            2
        )

        st.caption(
            f"FAILED ATTEMPTS: {st.session_state.room2_attempts}"
        )

    else:

        st.success("MESSAGE SUCCESSFULLY DECRYPTED.")

        st.markdown("## PASSWORD RECOVERED")

        st.markdown(
            f"""
            <div style="
                background:#17171d;
                border:1px solid #b99b65;
                padding:30px;
                text-align:center;
            ">
                <div style="
                    color:#b99b65;
                    font-family:monospace;
                    letter-spacing:4px;
                ">
                    RECOVERED PASSWORD
                </div>
                <div style="
                    color:#f0d8a8;
                    font-size:38px;
                    letter-spacing:6px;
                    font-family:monospace;
                ">
                    {html.escape(str(SECURITY_PASSWORD))}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write(
            "The encrypted transmission has been recovered. "
            "The second security checkpoint is now accessible."
        )

        st.info("ROOM 3 IS NOW UNLOCKED.")


# ---------------- ROOM 3: THE FINAL CHALLENGE ----------------

elif st.session_state.selected_room == "room3":

    st.divider()

    st.markdown(
        '<div class="terminal">ACCESSING FILE: EF-003-C</div>',
        unsafe_allow_html=True
    )

    st.markdown("# THE FINAL CHALLENGE")

    st.warning("FINAL SECURITY PROTOCOL ACTIVATED.")

    st.write("""
    You have reached the final stage of the investigation.

    One suspect is responsible for sabotaging the facility.
    Use the evidence below to identify the culprit.
    """)

    st.markdown("### SUSPECT DATABASE")

    st.write("""
    **Alex:** Was not responsible for the sabotage.

    **Jordan:** Was seen near the control room but was not responsible.

    **Morgan:** The remaining suspect.
    """)

    if not st.session_state.room3_completed:

        with st.form("final_challenge_form"):

            user_answer = st.text_input(
                "IDENTIFY THE CULPRIT",
                placeholder="Enter suspect name..."
            )

            submitted = st.form_submit_button(
                "SUBMIT FINAL ANSWER"
            )

            if submitted:

                if check_final_answer(user_answer):

                    finish_room(3)
                    st.rerun()

                else:

                    record_failed_attempt(3)

                    st.error("IDENTIFICATION FAILED.")

        st.divider()

        show_hint(
            "REQUEST INTELLIGENCE REPORT",
            FINAL_HINTS,
            3
        )

        st.caption(
            f"FAILED ATTEMPTS: {st.session_state.room3_attempts}"
        )

    else:

        st.success(
            "CULPRIT IDENTIFIED. FACILITY SECURITY OVERRIDDEN."
        )

        st.markdown("## FINAL SECURITY PHRASE")

        st.title(SECURITY_PHRASE)

        st.balloons()

        st.markdown("### MISSION COMPLETE")

        st.write("""
        All three security checkpoints have been overridden.

        The facility doors are unlocked. You have successfully escaped.
        """)


# ---------------- LEADERBOARD ----------------

st.divider()

st.markdown("## CLASSIFIED LEADERBOARD")

st.caption("TOP 10 AGENTS RANKED BY TOTAL SCORE.")

leaderboard = get_leaderboard()

if leaderboard:

    st.table([
        {
            "AGENT": player[0],
            "SCORE": player[1],
            "ROOMS COMPLETED": player[2],
            "LAST PLAYED": player[3]
        }
        for player in leaderboard
    ])

else:

    st.info("NO AGENT RECORDS FOUND.")


# ---------------- FOOTER ----------------

st.divider()

st.markdown(
    """
    <div style="text-align: center; padding: 20px 0; color: #888;">
        <p style="font-family: 'Share Tech Mono', monospace;">
            THE ENIGMA FILES
        </p>
        <p style="font-size: 12px;">
            CLASSIFIED INVESTIGATION SYSTEM
        </p>
        <p style="font-size: 11px;">
            © 2026 THE ENIGMA FILES. ALL RIGHTS RESERVED.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
