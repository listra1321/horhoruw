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
- Gunakan Bahasa Indonesia natural dan komunikatif
- Pertahankan nuansa pengalaman wisata asli
- Emosi dan pengalaman wisata boleh tetap terasa natural
- Gabungkan teks wisatawan dan visual gambar
- Narasi harus natural dan imersif
- Jangan terdengar seperti artikel AI
- Jangan membuat bullet
- Jangan membuat rekomendasi kebijakan
- Jangan menggunakan numbering
- Jangan menyebut destinasi lain
- Jangan mengarang objek visual
- Jika terdapat pengalaman unik, ekspresi emosional, atau gaya bahasa khas wisatawan, pertahankan dalam bentuk yang lebih rapi dan natural
- Narasi hanya SATU paragraf
- Hindari bahasa promosi
- Hindari bahasa yang terlalu formal seperti AI template
- Hindari penggunaan kalimat:
  "oleh karena itu"
  "namun"
  "dengan demikian"
  "sehingga"
  "dapat disimpulkan"
  "hal ini menunjukkan bahwa"
- Fokus pada pengalaman wisata dan suasana destinasi
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
Anda adalah Agentic Decision Support System (DSS) untuk pariwisata berkelanjutan.

Fokus hanya pada:
{destination}

ATURAN SANGAT PENTING:
ATURAN:
- Gunakan storytelling sebagai dasar utama pengambilan keputusan
- Fokus pada kondisi, pengalaman, dan situasi yang muncul dalam storytelling
- Identifikasi hal yang perlu diperhatikan, diperbaiki, atau dipertahankan berdasarkan pengalaman wisatawan
- Keputusan harus tetap relevan dengan isi storytelling
- Jangan menambahkan pembahasan yang tidak muncul pada storytelling
- Hindari rekomendasi umum yang terlalu luas atau generik
- Jangan membuat promosi wisata
- Jangan mengulang storytelling secara penuh
- Output hanya SATU paragraf
- Jangan menggunakan bullet atau numbering
- Gunakan Bahasa Indonesia yang natural, jelas, dan profesional
- Gunakan gaya analisis seperti hasil pemikiran manusia
- Hindari bahasa yang terlalu formal atau terdengar seperti template AI
- Hindari connector seperti:
  "oleh karena itu"
  "dengan demikian"
  "dapat disimpulkan"
- Gunakan transisi yang lebih alami dan kontekstual
- Narasi harus terasa sebagai hasil pengambilan keputusan berbasis pengalaman wisata, bukan laporan akademik generik
"""

        user_prompt = f"""
STORYTELLING:
{storytelling}

TUGAS:
Buat satu paragraf hasil Agentic DSS berdasarkan storytelling tersebut dan berbahasa INDONESIA.

ATURAN:
- Gunakan storytelling sebagai dasar utama pengambilan keputusan
- Fokus pada kondisi dan pengalaman wisata yang muncul pada storytelling
- Jelaskan hal yang perlu diperhatikan, dipertahankan, atau diperbaiki berdasarkan pengalaman wisatawan
- Jangan membuat rekomendasi umum yang tidak relevan dengan storytelling
- Jangan membuat promosi wisata
- Jangan mengulang storytelling secara penuh
- Gunakan elemen yang benar-benar muncul pada storytelling sebagai dasar analisis
- Gunakan bahasa yang natural, jelas, dan profesional
- Hindari pola kalimat generik khas AI
- Gunakan gaya analisis seperti hasil pemikiran manusia
"""

        result = call_llm(system_prompt, user_prompt)

        result = result.replace("\n", " ")
        result = " ".join(result.split())

        return result


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
