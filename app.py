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

/* Neon Button */
.stButton button {

    width: 100%;

    background: linear-gradient(
        90deg,
        #8B5CF6,
        #06B6D4
    );

    color: white;

    border: none;

    border-radius: 18px;

    padding: 18px;

    font-size: 18px;

    font-weight: 700;

    box-shadow:
        0 0 20px rgba(139,92,246,0.45);

    transition: 0.3s;
}

.stButton button:hover {

    transform: scale(1.02);

    box-shadow:
        0 0 35px rgba(6,182,212,0.55);
}

[data-testid="collapsedControl"] {
    display: none;
}

/* HIDE STREAMLIT HEADER */
header[data-testid="stHeader"]{
    display: none;
}

/* HIDE TOOLBAR */
[data-testid="stToolbar"]{
    display: none;
}

/* HIDE HAMBURGER */
#MainMenu{
    visibility: hidden;
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
import shap
import matplotlib.pyplot as plt

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

# ======================================================
# SHAP
# ======================================================

def predict_text(texts):

    classifier = load_sentiment()

    outputs = []

    for t in texts:

        result = classifier(t)[0]

        if result['label'] == 'positive':
            outputs.append([1-result['score'], result['score']])

        else:
            outputs.append([result['score'], 1-result['score']])

    return np.array(outputs)


def explain_with_shap(text):

    explainer = shap.Explainer(
        predict_text,
        masker=shap.maskers.Text()
    )

    shap_values = explainer([text])

    return shap_values

# =========================
# PASSWORD PROTECTION
# =========================
SYSTEM_PASSWORD = st.secrets.get("SYSTEM_PASSWORD")

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("🔐 Login Sistem ADSS Pariwisata")
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
            "brastagi",
            "sipiso",
            "simarjarunjung",
            "parapat",
            "lake"
        ],

        "Riam Berawan": [
            "riam",
            "berawan",
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

    # if len(detected_destinations) > 1:
    #     return False

    return True

# =========================
# UI
# =========================
# st.title(
#     "🌱 Storytelling Multimodal untuk Agentic Decision Support System Pariwisata"
# )

st.markdown("""
<div class='main-title'>
🌱 Storytelling Multimodal untuk Agentic Decision Support System Pariwisata
</div>


""", unsafe_allow_html=True)

text = st.text_area("📝 Masukkan teks wisata")

image_file = st.file_uploader("📷 Upload gambar")

# =========================
# VALIDASI DESTINASI (ANTI HALUSINASI DOMAIN)
# =========================
#DESTINASI_VALID = ["Danau Toba", "Candi Borobudur"]
DESTINASI_VALID = [
    "Danau Toba",
    "Candi Borobudur",
    "Riam Berawan",
    "Sepadang Hill"
]

destinasi = st.selectbox(
    "📍 Pilih Destinasi Wisata",
    DESTINASI_VALID
)

if destinasi not in DESTINASI_VALID:
    st.error("Destinasi tidak valid.")
    st.stop()

orch = AgentOrchestrator()

# =========================
# GENERATE
# =========================
#if st.button("🧠 Generate Storytelling & Agentic DSS"):
generate = st.button("🧠 Generate Storytelling & Agentic DSS")



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
        with st.spinner("🤖 Menghasilkan storytelling dan pengambilan keputusan..."):
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
        
        # st.write(f"{emoji} {story.strip()}") mematikan emoji
        st.write(story.strip())
        
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
 
        
        # ======================================================
        # XAI 1: INPUT EXPLANATION
        # ======================================================
        st.subheader("📊 XAI - Input Explanation")
        
        try:
            exp_input = explain_with_lime(text)
            explanation_input = exp_input.as_list()
        
            if not explanation_input:
                st.warning("⚠️ Tidak ada fitur input yang dapat dijelaskan.")
            else:
                for word, weight in explanation_input:
                    if weight > 0:
                        st.markdown(f"🟢 **{word}** → +{weight:.3f}")
                    else:
                        st.markdown(f"🔴 **{word}** → {weight:.3f}")
        
                st.caption("Kontribusi fitur input terhadap pembentukan storytelling")
                #st.components.v1.html(exp_input.as_html(), height=150)
                # lime_html = f"""
                # <style>
                # body {{
                #     background-color: #0F172A;
                #     color: white;
                # }}
                
                # div {{
                #     color: white !important;
                # }}
                
                # text {{
                #     fill: white !important;
                # }}
                
                # svg text {{
                #     fill: white !important;
                # }}
                
                # table {{
                #     color: white !important;
                # }}
                
                # </style>
                
                # {exp_input.as_html()}
                # """
                
                # st.components.v1.html(lime_html, height=450, scrolling=True)
                lime_html = f"""
                <style>
                
                body {{
                    background-color: white;
                
                    color: black;
                
                    padding: 15px;
                
                    font-family: Arial, sans-serif;
                }}
                
                .main-svg {{
                    background-color: white !important;
                }}
                
                text {{
                    fill: black !important;
                
                    color: black !important;
                }}
                
                div {{
                    color: black !important;
                }}
                
                table {{
                    color: black !important;
                }}
                
                </style>
                
                {exp_input.as_html()}
                """
                
                st.components.v1.html(
                    lime_html,
                    height=250,
                    scrolling=True
                )
        
        except Exception as e:
            st.error(f"Error Input XAI: {e}")
        
        st.divider()
        # ======================================================
        # XAI 2: STORYTELLING EXPLANATION
        # ======================================================
        st.subheader("📊 XAI - Storytelling Explanation")
        
        try:
            exp_story = explain_with_lime(story)
            explanation_story = exp_story.as_list()
        
            if not explanation_story:
                st.warning("⚠️ Tidak ada fitur storytelling yang dapat dijelaskan.")
            else:
                for word, weight in explanation_story:
                    if weight > 0:
                        st.markdown(f"🟢 **{word}** → +{weight:.3f}")
                    else:
                        st.markdown(f"🔴 **{word}** → {weight:.3f}")
        
                st.caption("Kontribusi kata dalam storytelling terhadap karakteristik narasi")
                #st.components.v1.html(exp_story.as_html(), height=280)
                # lime_html_story = f"""
                # <style>
                # body {{
                #     background-color: #0F172A;
                #     color: white;
                # }}
                
                # div {{
                #     color: white !important;
                # }}
                
                # text {{
                #     fill: white !important;
                # }}
                
                # svg text {{
                #     fill: white !important;
                # }}
                
                # table {{
                #     color: white !important;
                # }}
                
                # </style>
                
                # {exp_story.as_html()}
                # """
                
                # st.components.v1.html(lime_html_story, height=450, scrolling=True)
                lime_html_story = f"""
                <style>
                
                body {{
                    background-color: white;
                
                    color: black;
                
                    padding: 15px;
                
                    font-family: Arial, sans-serif;
                }}
                
                .main-svg {{
                    background-color: white !important;
                }}
                
                text {{
                    fill: black !important;
                
                    color: black !important;
                }}
                
                div {{
                    color: black !important;
                }}
                
                table {{
                    color: black !important;
                }}
                
                </style>
                
                {exp_story.as_html()}
                """
                
                st.components.v1.html(
                    lime_html_story,
                    height=250,
                    scrolling=True
                )
        
        except Exception as e:
            st.error(f"Error Story XAI: {e}")
            
        st.divider()

        # ======================================================
        # SHAP EXPLANATION
        # ======================================================
        
        st.subheader("📈 SHAP Explanation")
        
        try:
        
            shap_values = explain_with_shap(text)
        
            shap_html = f"""
            <div style="
                background-color:white;
                padding:15px;
                border-radius:12px;
            ">
            {shap.plots.text(shap_values[0], display=False)}
            </div>
            """
        
            st.components.v1.html(
                shap_html,
                height=400,
                scrolling=True
            )
        
        except Exception as e:
        
            st.error(f"SHAP Error: {e}")
    
    else:
        st.warning("⚠️ Mohon lengkapi teks dan gambar.")

# ======================================================
# Footer
# ======================================================
st.markdown("---")
st.caption(
    "Catatan: Sistem ini merupakan prototipe Agentic Decision Support System "
    "dan tidak menggantikan kewenangan pengambil keputusan."
)
