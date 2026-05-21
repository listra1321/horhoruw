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
- Jangan terlalu formal seperti artikel akademik
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
- Hindari kalimat terlalu sempurna dan terlalu formal
- Pertahankan nuansa pengalaman manusia
- Gunakan gaya narasi wisata yang natural
- Jangan menggunakan kalimat promosi seperti "sangat direkomendasikan"
- Jika ada pengalaman unik dari wisatawan, pertahankan maknanya secara natural
- Fokus pada pengalaman wisata dan suasana destinasi
"""

        user_prompt = f"""
INPUT TEKS:
{text}

DESKRIPSI GAMBAR:
{caption}

TUGAS:
Buat storytelling multimodal dalam satu paragraf yang menyatukan pengalaman wisatawan dan suasana visual destinasi secara alami.
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
- Gunakan HANYA informasi yang muncul pada storytelling
- DILARANG menambahkan konsep baru yang tidak ada pada storytelling
- Jangan menambahkan:
  - infrastruktur
  - promosi
  - strategi umum
  - ekonomi
  - fasilitas
  jika tidak disebut dalam storytelling
- Analisis harus grounded pada narasi wisata
- Gunakan gaya akademik formal
- Output hanya SATU paragraf
- Jangan bullet
- Jangan numbering
- Jangan mengulang storytelling sepenuhnya
- Fokus pada interpretasi DSS dari pengalaman wisata dan implikiasi pengelolaannya
- Gunakan gaya akademik yang natural dan reflektif
- Hindari bahasa yang terlalu formal seperti AI template
- Hindari connector AI seperti:
  "oleh karena itu"
  "namun"
  "dengan demikian"
  "sehingga"
  "dapat disimpulkan"
  "hal ini menunjukkan bahwa"
- Gunakan transisi yang lebih alami dan manusiawi
- Narasi harus terasa seperti hasil analisis peneliti
- DSS harus menjelaskan:
  - karakteristik destinasi,
  - arah pengelolaan,
  - implikasi pengembangan wisata,
  berdasarkan storytelling
- Jangan terdengar seperti laporan akademik generik
"""

        user_prompt = f"""
STORYTELLING:
{storytelling}

TUGAS:
Buat satu paragraf hasil Agentic DSS berdasarkan storytelling tersebut.

ATURAN:
- Jangan menceritakan ulang storytelling
- Jangan membuat rekomendasi poin
- Jangan membuat promosi wisata
- Gunakan storytelling sebagai dasar reasoning
- Jelaskan keputusan atau arah pengelolaan destinasi secara natural
- Fokus pada interpretasi strategis ekowisata
- Gunakan elemen yang muncul pada storytelling sebagai dasar analisis
- Gunakan bahasa yang lebih natural dan tidak kaku
- Hindari pola kalimat generik khas AI
- Gunakan gaya analisis reflektif seperti peneliti manusia
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
