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

/* Background */
.stApp {
    background-color: #F5F7FA;
}

/* Main Container */
.main .block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

.stButton {
    width: 100%;
}

.stButton button {
    width: 100%;
}

.result-box {
    line-height: 1.8;
}

/* Title */
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #1E293B;
    margin-bottom: 10px;
}

.subtitle {
    font-size: 18px;
    color: #64748B;
    margin-bottom: 35px;
}

/* Card Style */
.custom-card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    margin-bottom: 25px;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #10B981, #059669);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 24px;
    font-size: 16px;
    font-weight: 600;
    transition: 0.3s;
}

.stButton>button:hover {
    background: linear-gradient(90deg, #059669, #047857);
    transform: scale(1.02);
}

/* Text Area */
textarea {
    border-radius: 12px !important;
}

/* Upload Box */
[data-testid="stFileUploader"] {
    background: white;
    padding: 15px;
    border-radius: 14px;
    border: 1px solid #E2E8F0;
}

/* Result Section */
.result-box {
    background: white;
    padding: 25px;
    border-radius: 18px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    margin-top: 20px;
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
#     "🌿 Storytelling Multimodal untuk Agentic Decision Support System Pariwisata"
# )

st.markdown("""
<div class='main-title'>
🌿 Storytelling Multimodal untuk Agentic Decision Support System Pariwisata
</div>

<div class='subtitle'>
Integrasi storytelling multimodal berbasis Large Language Models untuk mendukung pengambilan keputusan pariwisata.
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
    "Riam Berawan't",
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
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
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
