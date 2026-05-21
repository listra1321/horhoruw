import streamlit as st
st.set_page_config(
    page_title="Agentic DSS Pariwisata",
    page_icon="🌱",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>
.stApp {

    background:
        radial-gradient(circle at top left, rgba(59,130,246,0.18), transparent 30%),
        radial-gradient(circle at bottom right, rgba(168,85,247,0.18), transparent 30%),
        linear-gradient(135deg, #020617, #0F172A);

    color: white;
    animation: bgMove 15s ease infinite;
}

@keyframes bgMove {

    0% {
        background-position: left;
    }

    50% {
        background-position: right;
    }

    100% {
        background-position: left;
    }
}

/* Main Container */
.main .block-container {
    padding-top: 2rem;
    padding-left: 4rem;
    padding-right: 4rem;
}

/* Glass Card */
.custom-card {

    background: rgba(15, 23, 42, 0.55);

    backdrop-filter: blur(14px);

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 24px;

    padding: 28px;

    box-shadow:
        0 0 30px rgba(59,130,246,0.12),
        0 0 60px rgba(168,85,247,0.08);

    margin-bottom: 25px;
}

/* Result Box */
.result-box {

    background: rgba(15, 23, 42, 0.55);

    backdrop-filter: blur(14px);

    border: 1px solid rgba(255,255,255,0.08);

    border-radius: 24px;

    padding: 28px;

    box-shadow:
        0 0 30px rgba(59,130,246,0.12);

    margin-top: 30px;

    line-height: 1.9;
}

/* =========================================
HERO SECTION
========================================= */

.hero-badge {

    display: inline-block;

    padding: 8px 18px;

    border-radius: 999px;

    background: rgba(168,85,247,0.18);

    color: #C084FC;

    font-size: 13px;

    font-weight: 700;

    letter-spacing: 1px;

    margin-bottom: 18px;

    border: 1px solid rgba(168,85,247,0.35);
}

/* =========================================
TITLE
========================================= */

.hero-title {

    font-size: 48px;

    font-weight: 800;

    line-height: 1.15;

    background: linear-gradient(
        90deg,
        #C084FC,
        #38BDF8
    );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    margin-bottom: 24px;

    text-shadow:
        0 0 25px rgba(168,85,247,0.25);
}

/* =========================================
SUBTITLE
========================================= */

.hero-subtitle {

    font-size: 22px;

    line-height: 1.8;

    color: #CBD5E1;

    max-width: 850px;
}

img {

    animation: floating 4s ease-in-out infinite;
}



@keyframes floating {

    0% {
        transform: translateY(0px);
    }

    50% {
        transform: translateY(-10px);
    }

    100% {
        transform: translateY(0px);
    }
}

/* Title */
.main-title {

    font-size: 48px;
    line-height: 1.2;

    font-weight: 800;

    background: linear-gradient(
        90deg,
        #A855F7,
        #38BDF8
    );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    margin-bottom: 10px;
}

.main-title {

    text-shadow:
        0 0 25px rgba(168,85,247,0.35);
}

/* Subtitle */
.subtitle {

    font-size: 20px;

    color: #CBD5E1;

    margin-bottom: 35px;
}

/* Text */
label, p, div {

    color: #E2E8F0 !important;
}

/* Text Area */
textarea {

    background: rgba(15,23,42,0.85) !important;

    color: #F8FAFC !important;

    border: 1px solid rgba(56,189,248,0.35) !important;

    border-radius: 18px !important;

    padding: 18px !important;

    font-size: 16px !important;

    min-height: 170px !important;

    padding: 24px !important;

    font-size: 18px !important;

    line-height: 1.8 !important;

    box-shadow:
        0 0 18px rgba(59,130,246,0.12);

}

/* Selectbox */
.stSelectbox div[data-baseweb="select"] {

    background: rgba(15,23,42,0.7);

    border-radius: 14px;
}

div[data-baseweb="select"] {

    background: rgba(15,23,42,0.82) !important;

    border: 1px solid rgba(56,189,248,0.25);

    border-radius: 14px;

    color: white !important;
}

/* Upload */
[data-testid="stFileUploader"] {

    background: rgba(15,23,42,0.55);

    border: 1px dashed rgba(56,189,248,0.55);

    border-radius: 20px;

    padding: 18px;

    box-shadow:
        0 0 18px rgba(59,130,246,0.08);
}

/* destinasi */
[data-testid="stSelectbox"] {

    background: rgba(15,23,42,0.55);

    border: 1px dashed rgba(56,189,248,0.55);

    border-radius: 20px;

    padding: 18px;

    box-shadow:
        0 0 18px rgba(59,130,246,0.08);
}

/* Neon Button */
.stButton button {

    background:
        linear-gradient(
            90deg,
            #8B5CF6,
            #06B6D4
        );

    color: white;

    border: none;

    border-radius: 18px;

    height: 68px;

    width: 100%;

    font-size: 22px;

    font-weight: 700;

    box-shadow:
        0 0 35px rgba(139,92,246,0.35);

    transition: 0.3s ease;
}

.stButton button:hover {

    transform: scale(1.02);

    box-shadow:
        0 0 35px rgba(6,182,212,0.55);
}

[data-testid="collapsedControl"] {
    display: none;
}

/* =========================================
ROBOT CONTAINER
========================================= */

.robot-container {

    display: flex;

    justify-content: center;

    align-items: center;

    margin-top: 40px;
}

/* =========================================
ROBOT IMAGE
========================================= */

.robot-container img {

    filter:
        drop-shadow(0 0 25px rgba(168,85,247,0.45));

    animation:
        floatingRobot 4s ease-in-out infinite;
}

/* =========================================
FLOATING ANIMATION
========================================= */

@keyframes floatingRobot {

    0% {
        transform: translateY(0px);
    }

    50% {
        transform: translateY(-12px);
    }

    100% {
        transform: translateY(0px);
    }
}

.robot-container {

    position: relative;
}

.robot-container::before {

    content: "";

    position: absolute;

    width: 320px;
    height: 320px;

    border-radius: 50%;

    background:
        radial-gradient(
            circle,
            rgba(168,85,247,0.25),
            transparent 70%
        );

    filter: blur(40px);

    z-index: -1;
}

/* =========================================
GLASS CARD
========================================= */

.glass-card {

    background:
        linear-gradient(
            135deg,
            rgba(10,15,35,0.82),
            rgba(20,30,60,0.45)
        );

    border:
        1px solid rgba(255,255,255,0.08);

    border-radius: 28px;

    padding: 28px;

    margin-bottom: 30px;

    backdrop-filter: blur(22px);

    box-shadow:
        0 10px 40px rgba(0,0,0,0.35);
}

/* =========================================
SECTION TITLE
========================================= */

.section-title {

    font-size: 22px;

    font-weight: 700;

    color: #E2E8F0;

    margin-bottom: 15px;
}

/* =========================================
TEXT AREA
========================================= */

textarea {

    background:
        rgba(15,23,42,0.88) !important;

    color: white !important;

    border-radius: 18px !important;

    border:
        1px solid rgba(168,85,247,0.55) !important;

    box-shadow:
        0 0 25px rgba(168,85,247,0.18);

    font-size: 18px !important;
    padding: 20px !important;
}

/* =========================================
SELECT BOX
========================================= */

.stSelectbox div[data-baseweb="select"] {

    background:
        rgba(15,23,42,0.9);

    border-radius: 16px;
}

/* =========================================
UPLOAD BOX
========================================= */

[data-testid="stFileUploader"] {

    border:
        2px dashed rgba(0,212,255,0.35);

    border-radius: 18px;

    padding: 25px;

    background:
        rgba(15,23,42,0.35);
}

[data-testid="stFileUploader"] small {

    display: none;
}

/* =========================================
BUTTON
========================================= */

.stButton button {

    background:
        linear-gradient(
            90deg,
            #8B5CF6,
            #06B6D4
        );

    color: white;

    border: none;

    border-radius: 18px;

    height: 68px;

    font-size: 22px;

    font-weight: 700;

    box-shadow:
        0 0 35px rgba(139,92,246,0.35);

    transition: 0.3s ease;
}

.stButton button:hover {

    transform: scale(1.02);

    box-shadow:
        0 0 45px rgba(6,182,212,0.45);
}

footer {
    visibility: hidden;
}


</style>
""", unsafe_allow_html=True)
from PIL import Image
from orchestrator import AgentOrchestrator
from caption_lookup import CaptionLookup
import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or st.secrets["OPENROUTER_API_KEY"]

def map_sentiment_to_emoji(label):
    label = label.lower()

    if "positive" in label:
        return "😊"
    elif "negative" in label:
        return "😡"
    else:
        return "😐"

from transformers import pipeline
from lime.lime_text import LimeTextExplainer
import numpy as np

# =========================
# SENTIMENT MODEL
# =========================
@st.cache_resource
def load_sentiment():
    return pipeline(
        "sentiment-analysis",
        model="w11wo/indonesian-roberta-base-sentiment-classifier"
    )

def analyze_sentiment(text):
    classifier = load_sentiment()
    result = classifier(text)[0]
    return result['label'], result['score']

def predict_proba(texts):
    classifier = load_sentiment()
    results = []
    
    for t in texts:
        res = classifier(t)[0]
        score = res["score"]
        
        if res["label"] == "positive":
            results.append([1-score, score])
        else:
            results.append([score, 1-score])
    
    return np.array(results)


def explain_with_lime(text):
    explainer = LimeTextExplainer(class_names=["negatif", "positif"])
    
    exp = explainer.explain_instance(
        text,
        predict_proba,
        num_features=4,
        num_samples=50
    )
    
    return exp

# =========================
# PASSWORD PROTECTION
# =========================
SYSTEM_PASSWORD = st.secrets.get("SYSTEM_PASSWORD")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔐 Login Sistem DSS Ekowisata")
    st.markdown("Masukkan password untuk mengakses sistem.")

    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if password == SYSTEM_PASSWORD:
            st.session_state["authenticated"] = True
            st.success("Login berhasil!")
            st.rerun()
        else:
            st.error("Password salah.")

    st.stop()

from transformers import BlipProcessor, BlipForConditionalGeneration
import torch

@st.cache_resource
def load_blip():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

def generate_caption_blip(image):
    processor, model = load_blip()

    inputs = processor(images=image, return_tensors="pt")
    out = model.generate(**inputs)

    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption


# =========================
# LOAD CAPTION DATASET
# =========================
caption_db = CaptionLookup("data_caption.csv")

# =========================
# HELPER
# =========================
def detect_destination(text):
    text_lower = text.lower()

    if "toba" in text_lower:
        return "Danau Toba"
    elif "borobudur" in text_lower:
        return "Candi Borobudur"
    else:
        return "Destinasi Wisata"

# =====================================================
# VALIDASI MULTIMODAL DESTINASI
# =====================================================

def validate_destination(text, caption, destinasi):

    text_lower = text.lower()
    caption_lower = caption.lower()

    combined = text_lower + " " + caption_lower

    # =====================================================
    # KEYWORDS DESTINASI
    # =====================================================

    destination_keywords = {

        "Candi Borobudur": [
            "borobudur",
            "candi",
            "stupa",
            "temple"
        ],

        "Danau Toba": [
            "toba",
            "danau",
            "lake",
            "water"
        ],

        "Riam Berawan't": [
            "riam",
            "berawan't",
            "air terjun",
            "sungai",
            "arus"
        ],

        "Sepadang Hill": [
            "sepadang",
            "hill",
            "bukit",
            "perbukitan"
        ]
    }

    # =====================================================
    # DETEKSI DESTINASI
    # =====================================================

    detected_destinations = []

    for dest, keywords in destination_keywords.items():

        if any(k in combined for k in keywords):
            detected_destinations.append(dest)

    print("DETECTED DESTINATION:", detected_destinations)

    # =====================================================
    # TIDAK ADA YANG TERDETEKSI
    # =====================================================

    if len(detected_destinations) == 0:
        return False

    # =====================================================
    # DESTINASI TIDAK SESUAI PILIHAN
    # =====================================================

    if destinasi not in detected_destinations:
        return False

    # =====================================================
    # KONFLIK MULTI DESTINASI
    # =====================================================

    if len(detected_destinations) > 1:
        return False

    return True

# =========================
# UI
# =========================
# st.title(
#     "🌱 Storytelling Multimodal untuk Agentic Decision Support System Pariwisata"
# )

# st.markdown("""
# <div class='main-title'>
# 🌱 Storytelling Multimodal untuk Agentic Decision Support System Pariwisata
# </div>

# <div class='subtitle'>
# Integrasi storytelling multimodal berbasis Large Language Models untuk mendukung pengambilan keputusan pariwisata.
# </div>
# """, unsafe_allow_html=True)

col1, col2 = st.columns([2, 5])

with col1:

    st.markdown("<div class='robot-container'>", unsafe_allow_html=True)

    st.image(
        "robbot.png",
        width=380
    )

    st.markdown("</div>", unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class='hero-badge'>
        AI STORYTELLING ENGINE
    </div>

    <div class='hero-title'>
        Storytelling Multimodal untuk <br>
        Agentic Decision Support System Pariwisata
    </div>

    <div class='hero-subtitle'>
        Integrasi storytelling multimodal berbasis Large Language Models 
        untuk mendukung pengambilan keputusan pariwisata yang cerdas, 
        adaptif, dan berbasis data.
    </div>
    """, unsafe_allow_html=True)

# col1, col2 = st.columns([1, 2])

# with col1:

#     st.image(
#         "logo.png",
#         width=260
#     )

# with col2:

#     st.markdown("""
#     <div class='hero-badge'>
#         AI STORYTELLING ENGINE
#     </div>

#     <div class='hero-title'>
#         Storytelling Multimodal untuk <br>
#         Agentic Decision Support System Pariwisata
#     </div>

#     <div class='hero-subtitle'>
#         Integrasi storytelling multimodal berbasis Large Language Models 
#         untuk mendukung pengambilan keputusan pariwisata yang cerdas, 
#         adaptif, dan berbasis data.
#     </div>
#     """, unsafe_allow_html=True)


# text = st.text_area("📝 Masukkan teks wisata")

# image_file = st.file_uploader("📷 Upload gambar")

# # =========================
# # VALIDASI DESTINASI (ANTI HALUSINASI DOMAIN)
# # =========================
# #DESTINASI_VALID = ["Danau Toba", "Candi Borobudur"]
# DESTINASI_VALID = [
#     "Danau Toba",
#     "Candi Borobudur",
#     "Riam Berawan't",
#     "Sepadang Hill"
# ]

# destinasi = st.selectbox(
#     "📍 Pilih Destinasi Wisata",
#     DESTINASI_VALID
# )

# if destinasi not in DESTINASI_VALID:
#     st.error("Destinasi tidak valid.")
#     st.stop()

# orch = AgentOrchestrator()

# # =========================
# # GENERATE
# # =========================
# #if st.button("🧠 Generate Storytelling & Agentic DSS"):
# generate = st.button("🧠 Generate Storytelling & Agentic DSS")

# =====================================================
# TEXT INPUT
# =====================================================

st.markdown("""
<div class='section-title'>
📝 Masukkan Teks Wisata
</div>
""", unsafe_allow_html=True)

text = st.text_area(
    "",
    placeholder="Jelaskan destinasi, pengalaman, atau topik wisata yang ingin diceritakan...",
    height=170
)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# 2 COLUMN LAYOUT
# =====================================================

col1, col2 = st.columns([1.2, 1])

# =====================================================
# UPLOAD
# =====================================================

with col1:

    st.markdown("""
    <div class='glass-card'>
    <div class='section-title'>
    🖼️ Upload Gambar
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "",
        type=["jpg", "jpeg", "png", "webp"]
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# DESTINATION
# =====================================================

with col2:

    st.markdown("""
    <div class='glass-card'>
    <div class='section-title'>
    📍 Pilih Destinasi Wisata
    </div>
    """, unsafe_allow_html=True)

    destinasi = st.selectbox(
        "",
        [
            "Danau Toba",
            "Candi Borobudur",
            "Riam Berawant",
            "Sepadang Hill"
        ]
    )

    st.markdown("</div>", unsafe_allow_html=True)

# =====================================================
# BUTTON
# =====================================================

st.markdown("<br>", unsafe_allow_html=True)

col_btn1, col_btn2, col_btn3 = st.columns([1,2,1])

with col_btn2:

    generate = st.button(
        "🧠 Generate Storytelling & Agentic DSS",
        use_container_width=True
    )

if generate:

    if text and image_file:

        # tampilkan gambar (TETAP ADA)
        image = Image.open(image_file)
        st.image(image, width=240)

        # =========================
        # CAPTION (HANYA BACKEND)
        # =========================
        filename = image_file.name.lower().strip()
        caption = generate_caption_blip(image)

        # =========================
        # VALIDASI DESTINASI
        # =========================
        is_valid = validate_destination(text, caption, destinasi)

        if not is_valid:
            st.error("❌ Maaf, terdapat ketidaksesuaian antara teks, gambar, dan destinasi.")
            st.stop()

        # fallback kalau tidak ada
        if not caption:
            caption = f"Gambar berkaitan dengan konteks wisata: {text[:100]}"

        # =========================
        # SENTIMENT ANALYSIS
        # =========================
        sentiment_label, score = analyze_sentiment(text)
        emoji = map_sentiment_to_emoji(sentiment_label)

        # =========================
        # VALIDASI DESTINASI
        # =========================
    
        

        # =========================
        # MULTI-AGENT PROCESS
        # =========================
        with st.spinner("🤖 Menghasilkan storytelling dan kebijakan..."):
            result = orch.run(text, caption, destinasi)
            
        

        # =====================================================
        # OUTPUT
        # =====================================================
        
        st.divider()
        
        # =====================================================
        # SPLIT STORY & DSS
        # =====================================================
        
        if "###DSS###" in result:
            story, dss = result.split("###DSS###", 1)
        else:
            story = result
            dss = "Hasil DSS tidak tersedia."
        
        # =====================================================
        # STORYTELLING
        # =====================================================
        #st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.subheader("📄 Storytelling Wisata")
        
        st.write(f"{emoji} {story.strip()}")
        
        st.caption(
            "Narasi storytelling multimodal berdasarkan integrasi teks wisatawan dan interpretasi visual gambar."
        )
        
        st.divider()
        
        # =====================================================
        # AGENTIC DSS
        # =====================================================
        
        st.subheader("🧠 Hasil Agentic DSS")
        
        st.write(dss.strip())
        
        st.caption(
            "Hasil reasoning Agentic Decision Support System berbasis storytelling multimodal."
        )
        st.markdown("</div>", unsafe_allow_html=True)
 
        
    #     # ======================================================
    #     # XAI 1: INPUT EXPLANATION
    #     # ======================================================
    #     st.subheader("📊 XAI - Input Explanation")
        
    #     try:
    #         exp_input = explain_with_lime(text)
    #         explanation_input = exp_input.as_list()
        
    #         if not explanation_input:
    #             st.warning("⚠️ Tidak ada fitur input yang dapat dijelaskan.")
    #         else:
    #             for word, weight in explanation_input:
    #                 if weight > 0:
    #                     st.markdown(f"🟢 **{word}** → +{weight:.3f}")
    #                 else:
    #                     st.markdown(f"🔴 **{word}** → {weight:.3f}")
        
    #             st.caption("Kontribusi fitur input terhadap pembentukan storytelling")
    #             st.components.v1.html(exp_input.as_html(), height=150)
        
    #     except Exception as e:
    #         st.error(f"Error Input XAI: {e}")
        
    #     st.divider()
    #     # ======================================================
    #     # XAI 2: STORYTELLING EXPLANATION
    #     # ======================================================
    #     st.subheader("📊 XAI - Storytelling Explanation")
        
    #     try:
    #         exp_story = explain_with_lime(story)
    #         explanation_story = exp_story.as_list()
        
    #         if not explanation_story:
    #             st.warning("⚠️ Tidak ada fitur storytelling yang dapat dijelaskan.")
    #         else:
    #             for word, weight in explanation_story:
    #                 if weight > 0:
    #                     st.markdown(f"🟢 **{word}** → +{weight:.3f}")
    #                 else:
    #                     st.markdown(f"🔴 **{word}** → {weight:.3f}")
        
    #             st.caption("Kontribusi kata dalam storytelling terhadap karakteristik narasi")
    #             st.components.v1.html(exp_story.as_html(), height=280)
        
    #     except Exception as e:
    #         st.error(f"Error Story XAI: {e}")
    
    # else:
    #     st.warning("⚠️ Mohon lengkapi teks dan gambar.")

# ======================================================
# Footer
# ======================================================
st.markdown("---")
st.caption(
    "Catatan: Sistem ini merupakan prototipe Agentic Decision Support System "
    "dan tidak menggantikan kewenangan pengambil keputusan."
)
