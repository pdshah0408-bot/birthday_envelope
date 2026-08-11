"""
🎉 Happy Birthday Envelope 🎉
------------------------------------------------
A Streamlit app that shows an animated envelope.
Clicking it "opens" the envelope with a flap animation,
reveals a birthday wish, and a scattered polaroid-style
photo wall with your friend.

HOW TO RUN
  1. pip install streamlit
  2. streamlit run birthday_envelope.py

HOW TO CUSTOMIZE
  - Edit FRIEND_NAME, WISH_TITLE, WISH_MESSAGE, SIGNATURE below.
  - Add your own photos to a folder named "photos" next to this
    file (jpg/png), OR just use the uploader that appears once
    the envelope is opened.
"""

import base64
import os
import random
import streamlit as st
import streamlit.components.v1 as components

# ------------------------------------------------------------------
# ---------------------------  CONFIG  ------------------------------
# ------------------------------------------------------------------
FRIEND_NAME = "Kidooo"          # <-- change to their name
WISH_TITLE = "Happy Birthday!"
WISH_MESSAGE = """
Happiest Birthday, Kidddoooo! ❤️😭🫶🏻
Lovee you so muchhh! 🥹❤️

Forever grateful for the bond we share. No matter how much of a roller coaster this friendship becomes at times, you'll forever be my unwanted—oops, I mean adopted child 🤭😚

I've always felt that our bond is truly incredible. There have been so many times when I've learnt a lot from you, and I'm genuinely grateful to have this friendship in my life. No matter how much kalesh we do with each other, somehow, the kalesh we do with other people will always be my favourite kalesh 🤣😂😭

Here's to more memories, more nonsense, more fights, and obviously, more kalesh. 😂❤️
Stay the same annoying, amazing person you are. Happiest birthday once again, kiddooo! 🥹🫶🏻
"""
SIGNATURE = "With all my love,\nYour Best Friend 🎈"
PHOTO_FOLDER = "photos"   # put your images here (optional)

st.set_page_config(page_title=f"For {FRIEND_NAME} 💌", page_icon="🎂", layout="centered")

# ------------------------------------------------------------------
# --------------------------  SESSION  -------------------------------
# ------------------------------------------------------------------
if "opened" not in st.session_state:
    st.session_state.opened = False

def open_envelope():
    st.session_state.opened = True

# ------------------------------------------------------------------
# ---------------------------  STYLES  -------------------------------
# ------------------------------------------------------------------
st.markdown(
    """
<style>
#MainMenu, header, footer {visibility: hidden;}
.stApp {
    background: radial-gradient(circle at top, #2b1055 0%, #0f051d 70%);
    overflow-x: hidden;
}

/* floating confetti / sparkle background */
.sparkle-wrap {
    position: fixed; inset: 0; pointer-events: none; z-index: 0; overflow: hidden;
}
.sparkle {
    position: absolute; top: -5%; font-size: 22px; opacity: 0.85;
    animation: fall linear infinite;
}
@keyframes fall {
    0%   { transform: translateY(-10vh) rotate(0deg); opacity: 0; }
    10%  { opacity: 1; }
    100% { transform: translateY(110vh) rotate(360deg); opacity: 0.9; }
}

/* Envelope */
.envelope-stage {
    display: flex; justify-content: center; align-items: center;
    margin-top: 40px; position: relative; z-index: 1;
}
.envelope {
    position: relative;
    width: 320px; height: 210px;
    cursor: pointer;
    animation: bob 2.4s ease-in-out infinite;
}
@keyframes bob {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}
.env-body {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%;
    background: linear-gradient(135deg, #fff6e5, #ffe9c7);
    border-radius: 10px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.45);
}
.env-pocket-left, .env-pocket-right {
    position: absolute; top: 0; width: 0; height: 0;
    border-style: solid;
}
.env-pocket-left {
    left: 0;
    border-width: 105px 160px 105px 0;
    border-color: transparent #ffe0aa transparent transparent;
    opacity: 0.9;
}
.env-pocket-right {
    right: 0;
    border-width: 105px 0 105px 160px;
    border-color: transparent transparent transparent #ffe0aa;
    opacity: 0.9;
}
.env-flap {
    position: absolute; top: 0; left: 0; width: 0; height: 0;
    border-style: solid;
    border-width: 105px 160px 0 160px;
    border-color: #ffd699 transparent transparent transparent;
    transform-origin: top center;
    transition: transform 0.8s cubic-bezier(.4,1.4,.4,1);
    z-index: 3;
}
.envelope.open .env-flap {
    transform: rotateX(180deg);
}
.env-seal {
    position: absolute; top: 78px; left: 50%; transform: translate(-50%, 0);
    width: 54px; height: 54px; border-radius: 50%;
    background: radial-gradient(circle at 35% 30%, #ff6b6b, #b5121b);
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 22px; box-shadow: 0 4px 10px rgba(0,0,0,0.4);
    z-index: 4; transition: opacity 0.4s ease;
}
.envelope.open .env-seal { opacity: 0; }
.env-hint {
    text-align: center; color: #f3e6ff; opacity: 0.85; margin-top: 18px;
    font-size: 15px; letter-spacing: 0.5px;
}

/* Letter card */
.letter-wrap {
    display: flex; justify-content: center; margin-top: 10px;
}
.letter-card {
    max-width: 640px; width: 100%;
    background: linear-gradient(180deg, #fffdf8, #fff3e0);
    border-radius: 16px; padding: 36px 40px;
    box-shadow: 0 25px 60px rgba(0,0,0,0.5);
    animation: rise 0.9s ease forwards;
    position: relative; z-index: 2;
}
@keyframes rise {
    from { opacity: 0; transform: translateY(60px) scale(0.96); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
}
.letter-title {
    text-align: center; font-size: 40px; margin-bottom: 4px;
    background: linear-gradient(90deg, #ff5f6d, #ffc371, #ff5f6d);
    -webkit-background-clip: text; background-clip: text; color: transparent;
    animation: shimmer 3s linear infinite; background-size: 200% auto;
}
@keyframes shimmer { to { background-position: 200% center; } }
.letter-sub { text-align: center; color: #a67c52; margin-bottom: 22px; font-style: italic;}
.letter-body {
    font-size: 17px; line-height: 1.75; color: #4a3a2c; white-space: pre-line;
}
.letter-sign {
    margin-top: 22px; text-align: right; font-size: 16px; color: #7a5230;
    white-space: pre-line; font-style: italic;
}
.balloon {
    position: fixed; bottom: -60px; font-size: 34px; opacity: 0.9;
    animation: floatUp linear forwards; z-index: 0;
}
@keyframes floatUp {
    to { transform: translateY(-120vh) translateX(20px) rotate(15deg); opacity: 0; }
}
.photo-title {
    text-align: center; color: #ffe9c7; font-size: 24px; margin: 34px 0 26px 0;
}
.wall-hint {
    text-align: center; color: #d8c7ff; opacity: 0.75; font-size: 13px;
    margin-top: -10px; margin-bottom: 6px; font-style: italic;
}
</style>
""",
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# ---------------------  FLOATING BACKGROUND  -------------------------
# ------------------------------------------------------------------
def sparkle_bg(n=22):
    emojis = ["🎈", "✨", "🎉", "💛", "🎊"]
    spans = ""
    for i in range(n):
        left = random.randint(0, 100)
        dur = round(random.uniform(6, 14), 1)
        delay = round(random.uniform(0, 8), 1)
        size = random.randint(16, 28)
        e = random.choice(emojis)
        spans += (
            f'<span class="sparkle" style="left:{left}%; font-size:{size}px; '
            f'animation-duration:{dur}s; animation-delay:{delay}s;">{e}</span>'
        )
    st.markdown(f'<div class="sparkle-wrap">{spans}</div>', unsafe_allow_html=True)

sparkle_bg()

# ------------------------------------------------------------------
# -----------------------------  UI  ----------------------------------
# ------------------------------------------------------------------
if not st.session_state.opened:
    st.markdown(
        f"""
        <div class="envelope-stage">
          <div class="envelope">
            <div class="env-body"></div>
            <div class="env-pocket-left"></div>
            <div class="env-pocket-right"></div>
            <div class="env-flap"></div>
            <div class="env-seal">💌</div>
          </div>
        </div>
        <div class="env-hint">A little something for {FRIEND_NAME} — tap the button below to open ↓</div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.button("💌 Open the envelope", on_click=open_envelope, use_container_width=True)

else:
    # balloons rising
    balloon_html = ""
    for i in range(10):
        left = random.randint(2, 95)
        dur = round(random.uniform(5, 10), 1)
        delay = round(random.uniform(0, 4), 1)
        balloon_html += (
            f'<span class="balloon" style="left:{left}%; '
            f'animation-duration:{dur}s; animation-delay:{delay}s;">🎈</span>'
        )
    st.markdown(balloon_html, unsafe_allow_html=True)
    st.balloons()

    st.markdown(
        f"""
        <div class="letter-wrap">
          <div class="letter-card">
            <div class="letter-title">{WISH_TITLE} 🎂</div>
            <div class="letter-sub">To my dearest {FRIEND_NAME}</div>
            <div class="letter-body">{WISH_MESSAGE}</div>
            <div class="letter-sign">{SIGNATURE}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="photo-title">📸 Our Chaotic, Iconic Memories</div>', unsafe_allow_html=True)
    st.markdown('<div class="wall-hint">hover a photo to zoom in ✨</div>', unsafe_allow_html=True)

    def _b64(data: bytes) -> str:
        return base64.b64encode(data).decode("utf-8")

    def render_polaroid_wall(images_bytes):
        """images_bytes: list of raw image bytes.

        Rendered through components.html (a real iframe) instead of
        st.markdown, because st.markdown runs content through a markdown
        parser first -- and that parser can choke on very long, no-break
        base64 image strings, silently dropping every photo after the
        first one. An iframe just gets raw HTML, so nothing gets lost.
        """
        random.seed(7)  # keep the scatter consistent between reruns
        tiles = ""
        for img_bytes in images_bytes:
            rot = round(random.uniform(-9, 9), 1)
            tape_rot = round(random.uniform(-25, 25), 1)
            b64 = _b64(img_bytes)
            tiles += f"""
            <div class="polaroid" style="--rot:{rot}deg; transform: rotate({rot}deg);">
                <div class="tape" style="--tape-rot:{tape_rot}deg;"></div>
                <img src="data:image/jpeg;base64,{b64}" />
            </div>
            """

        rows = -(-len(images_bytes) // 3)  # ceil division, ~3 photos per row
        height = max(320, rows * 260 + 40)

        page = f"""
        <html>
        <head>
        <style>
            html, body {{
                margin: 0; padding: 0; background: transparent;
                font-family: sans-serif;
            }}
            .polaroid-wall {{
                display: flex; flex-wrap: wrap; justify-content: center;
                gap: 26px 22px; max-width: 760px; margin: 0 auto; padding: 10px;
            }}
            .polaroid {{
                background: #fffdf9;
                padding: 14px 14px 34px 14px;
                width: 190px;
                border-radius: 3px;
                box-shadow: 0 10px 22px rgba(0,0,0,0.45);
                position: relative;
                opacity: 0;
                animation: polaroidIn 0.6s ease forwards;
                transition: transform 0.35s ease, box-shadow 0.35s ease, z-index 0s;
            }}
            .polaroid:hover {{
                transform: rotate(0deg) scale(1.12) !important;
                box-shadow: 0 24px 45px rgba(0,0,0,0.6);
                z-index: 50;
            }}
            @keyframes polaroidIn {{
                from {{ opacity: 0; transform: translateY(24px) scale(0.8) rotate(0deg); }}
                to   {{ opacity: 1; transform: translateY(0) scale(1) rotate(var(--rot)); }}
            }}
            .polaroid img {{
                width: 100%; height: 190px; object-fit: cover; display: block;
                border: 1px solid #eee;
            }}
            .polaroid .tape {{
                position: absolute; top: -14px; left: 50%;
                width: 70px; height: 26px; margin-left: -35px;
                background: rgba(255, 236, 179, 0.75);
                border: 1px solid rgba(200,170,90,0.4);
                box-shadow: 0 2px 4px rgba(0,0,0,0.25);
                transform: rotate(var(--tape-rot));
            }}
        </style>
        </head>
        <body>
            <div class="polaroid-wall">{tiles}</div>
        </body>
        </html>
        """
        components.html(page, height=height, scrolling=False)

    # ---- Photos: load from ./photos folder if present, else let user upload ----
    photo_paths = []
    if os.path.isdir(PHOTO_FOLDER):
        for f in sorted(os.listdir(PHOTO_FOLDER)):
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                photo_paths.append(os.path.join(PHOTO_FOLDER, f))

    if photo_paths:
        images_bytes = []
        for p in photo_paths:
            with open(p, "rb") as fh:
                images_bytes.append(fh.read())
        render_polaroid_wall(images_bytes)
    else:
        st.info(
            f"No photos found in a `{PHOTO_FOLDER}/` folder next to this script. "
            "Upload a few below to pin them to the wall! (They won't be saved after you close the app.)"
        )
        uploaded = st.file_uploader(
            "Upload photos of you two",
            type=["jpg", "jpeg", "png", "webp"],
            accept_multiple_files=True,
        )
        if uploaded:
            render_polaroid_wall([f.getvalue() for f in uploaded])

    st.markdown(
        "<p style='text-align:center; color:#f3e6ff; margin-top:26px;'>🎊 Happy Birthday, "
        f"{FRIEND_NAME}! 🎊</p>",
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("↺ Close envelope again", use_container_width=True):
            st.session_state.opened = False
            st.rerun()