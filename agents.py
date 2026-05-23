import os
import streamlit as st
import requests

# =====================================================
# API CONFIG
# =====================================================

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]

MODEL = "meta-llama/llama-3-8b-instruct"

# =====================================================
# GENERIC LLM CALL
# =====================================================

def call_llm(system_prompt, user_prompt):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "temperature": 0.3
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    try:
        res = response.json()

        if "choices" in res:
            return res["choices"][0]["message"]["content"]

        elif "error" in res:
            return f"API ERROR: {res['error']['message']}"

        else:
            return str(res)

    except Exception as e:
        return str(e)


# =====================================================
# STORYTELLING AGENT
# =====================================================

class StorytellingAgent:

    def run(self, text, caption, destination):

        system_prompt = f"""
Anda adalah Storytelling Agent multimodal pada sistem pariwisata berbasis Large Language Models.

Fokus hanya pada destinasi:
{destination}

ATURAN:
- Gunakan Bahasa Indonesia
- Output hanya SATU paragraf
- Buat deskripsi naratif berdasarkan teks wisatawan dan gambar
- Gunakan hanya informasi yang benar-benar muncul pada input
- Jangan menambahkan imajinasi, metafora, atau cerita tambahan
- Jangan membuat narasi puitis, dramatis, atau emosional berlebihan
- Jangan menggunakan gaya novel, cerita rakyat, atau travel blogger
- Jangan menambahkan detail yang tidak terlihat pada gambar atau teks
- Gunakan gaya bahasa sederhana, natural, dan informatif
- Fokus pada kondisi perjalanan, suasana lokasi, dan pengalaman wisatawan
- Jangan membuat kesimpulan berlebihan
"""

        user_prompt = f"""
INPUT TEKS:
{text}

DESKRIPSI GAMBAR:
{caption}

TUGAS:
Buat storytelling multimodal dalam satu paragraf yang menyatukan pengalaman wisatawan dan suasana visual destinasi secara alami dan berbahasa INDONESIA.
"""

        result = call_llm(system_prompt, user_prompt)

        result = result.replace("\n", " ")
        result = " ".join(result.split())

        return result


# =====================================================
# DSS AGENT
# =====================================================

class DSSAgent:

    def run(self, storytelling, destination):

        system_prompt = f"""
    Anda adalah sistem kecerdasan buatan murni (Agentic Decision Support System) yang bertugas mengekstrak keputusan tata kelola destinasi wisata berbasis bukti empiris pengalaman wisatawan.
    
    Fokus Analisis: {destination}
    
    BATASAN KETAT (CRITICAL CONSTRAINTS):
    1. HANYA gunakan fakta eksplisit dari teks STORYTELLING. Jangan berasumsi, memproyeksi, atau menambah isu baru (seperti sampah, akses jalan, masyarakat lokal, ekowisata) jika tidak tertulis di STORYTELLING.
    2. JANGAN mengulang narasi/cerita ulang pengalaman wisatawan. Sifat output adalah ANALISIS REKOMENDASI MANAJEMEN.
    3. JANGAN membuat kalimat promosi, brosur, atau narasi estetis baru.
    4. GAYA BAHASA: Gunakan Bahasa Indonesia yang lugas, profesional, analitis, namun mengalir natural (human-like).
    5. OUTPUT: Wajib berupa SATU PARAGRAF padat (maksimal 3-4 kalimat).
    
    LARANGAN KERAS:
    - Jangan gunakan kata penghubung template AI: "oleh karena itu", "dengan demikian", "dapat disimpulkan", "berdasarkan hal tersebut", "kesimpulannya".
    - Jangan gunakan istilah jargon akademis yang terlalu luas/mengambang jika tidak relevan dengan teks.
    """
    
        user_prompt = f"""
    BERIKUT ADALAH DATA UTAMA YANG WAJIB DIANALSIS:
    STORYTELLING: 
    "{storytelling}"
    
    TUGAS ANDA:
    Hasilkan satu paragraf analisis keputusan pengelolaan destinasi (DSS) dengan formula terstruktur berikut (kerjakan secara implisit dalam satu paragraf):
    1. Identifikasi aspek utama yang memicu kepuasan wisatawan dari storytelling (apa yang berhasil/bagus).
    2. Tentukan keputusan tata kelola operasional untuk mempertahankan/menjaga aspek tersebut agar tidak rusak oleh overtourism atau salah kelola.
    
    CONTOH OUTPUT YANG BENAR (Gunakan gaya bahasa seperti ini):
    "Manajemen {destination} harus memprioritaskan pemeliharaan atmosfer area sekitar dan perlindungan visual kemegahan arsitektur untuk mempertahankan daya tarik utama berupa kenyamanan suasana dan estetika visual yang dirasakan wisatawan. Keputusan taktis perlu diarahkan pada pengaturan alur pengunjung di titik-titik swafoto favorit agar keasrian lingkungan dan kelegaan ruang tetap terjaga tanpa mengurangi kebebasan wisatawan dalam mengabadikan momen."
    
    Instruksi: Sesuai dengan format contoh di atas, buatlah hasil Agentic DSS untuk {destination} sekarang dalam satu paragraf tanpa kata terlarang.
    """
    
        result = call_llm(system_prompt, user_prompt)
        
        # Post-processing untuk memastikan kebersihan format
        result = result.replace("\n", " ")
        result = " ".join(result.split())
        
        return result

# class DSSAgent:

#     def run(self, storytelling, destination):

#         system_prompt = f"""
#     Anda adalah Agentic Decision Support System (DSS) untuk pariwisata indonesia.
    
#     Fokus hanya pada:
#     {destination}
    
#     ATURAN PENTING:
#     - Gunakan hanya informasi yang muncul pada storytelling
#     - Jangan menambahkan konsep baru yang tidak ada pada storytelling
#     - Jangan membuat promosi wisata
#     - Jangan mengulang storytelling
#     - Jangan menjadi narasi wisata lagi
#     - Output hanya satu paragraf
#     - Gunakan Bahasa Indonesia yang natural dan reflektif
#     - Fokus pada pengambilan keputusan berdasarkan pengalaman wisatawan
#     - DSS harus menjelaskan hal yang perlu dipertahankan, diperhatikan, atau diperbaiki berdasarkan pengalaman wisata
#     - Gunakan detail pengalaman wisata sebagai dasar analisis
#     - Hindari istilah akademik umum yang tidak relevan dengan storytelling
#     - Hindari bahasa template AI seperti:
#       "oleh karena itu"
#       "dengan demikian"
#       "dapat disimpulkan"
#     """
    
#         user_prompt = f"""
#     STORYTELLING:
#     {storytelling}
    
#     TUGAS:
#     Buat satu paragraf hasil Agentic DSS berdasarkan storytelling tersebut.
    
#     Fokus pada:
#     - keputusan pengelolaan destinasi,
#     - hal penting dari pengalaman wisatawan,
#     - aspek yang perlu dijaga atau diperhatikan,
#     berdasarkan storytelling.
    
#     Jangan membuat storytelling baru.
#     """
    
#         result = call_llm(system_prompt, user_prompt)
    
#         result = result.replace("\n", " ")
#         result = " ".join(result.split())
    
#         return result


# =====================================================
# AGENTIC CONTROL
# =====================================================

def check_issues(result, destination):

    issues = []

    if destination not in result:
        issues.append("DESTINATION_MISSING")

    if len(result) < 150:
        issues.append("TOO_SHORT")

    forbidden = [
        "1.",
        "2.",
        "3.",
        "•",
        "Rekomendasi",
        "\n\n"
    ]

    for f in forbidden:
        if f in result:
            issues.append("INVALID_FORMAT")

    hallucinations = [
        "ancient city",
        "old ruins",
        "guatemala",
        "machu picchu",
        "reruntuhan kota"
    ]

    for h in hallucinations:
        if h.lower() in result.lower():
            issues.append("HALLUCINATION")

    return list(set(issues))


# =====================================================
# REFINE AGENT
# =====================================================

def refine_output(result, issues, destination):

    system_prompt = """
Anda adalah Refiner Agent untuk memperbaiki kualitas narasi DSS.
"""

    user_prompt = f"""
PERBAIKI TEKS BERIKUT:

{result}

MASALAH:
{issues}

ATURAN:
- Fokus pada destinasi {destination}
- Output hanya SATU paragraf
- Jangan gunakan bullet
- Jangan gunakan numbering
- Gunakan gaya akademik formal
- Jangan mengubah makna utama
- Buat lebih natural dan konsisten
"""

    refined = call_llm(system_prompt, user_prompt)

    refined = refined.replace("\n", " ")
    refined = " ".join(refined.split())

    return refined


# =====================================================
# UNIFIED MULTI AGENT DSS
# =====================================================

class UnifiedAgent:

    def __init__(self, memory=None):

        self.story_agent = StorytellingAgent()
        self.dss_agent = DSSAgent()

    def run(self, text, caption, destination):

        # =====================================================
        # STEP 1 — STORYTELLING
        # =====================================================

        storytelling = self.story_agent.run(
            text,
            caption,
            destination
        )

        # =====================================================
        # STEP 2 — DSS REASONING
        # =====================================================

        dss_result = self.dss_agent.run(
            storytelling,
            destination
        )

        # =====================================================
        # STEP 3 — AGENTIC CONTROL
        # =====================================================

        max_iter = 2

        for i in range(max_iter):

            issues = check_issues(
                dss_result,
                destination
            )

            print(f"AGENTIC LOOP {i}:", issues)

            if not issues:
                break

            dss_result = refine_output(
                dss_result,
                issues,
                destination
            )

        # =====================================================
        # FINAL OUTPUT
        # =====================================================

        final_output = f"""
{storytelling}

###DSS###

{dss_result}
"""

        return final_output
