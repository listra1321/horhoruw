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
- Gunakan Bahasa Indonesia.
- Output hanya satu paragraf.
- Gabungkan informasi teks wisatawan dan informasi visual menjadi satu pengalaman perjalanan yang utuh.
- Anggap informasi visual sebagai bagian dari kejadian yang dialami wisatawan.
- Jangan menjelaskan gambar.
- Jangan menyebut kata:
  gambar,
  foto,
  caption,
  visual,
  terlihat pada gambar,
  gambar menunjukkan,
  foto menunjukkan,
  berdasarkan gambar.
- Tulis dari sudut pandang pengalaman perjalanan wisata.
- Fokus pada aktivitas, kondisi lokasi, suasana, dan pengalaman wisatawan.
- Gunakan hanya informasi yang tersedia pada teks dan gambar.
- Jangan berimajinasi.
- Jangan menambahkan objek yang tidak muncul pada input.
- Jangan membuat cerita fiksi.
- Jangan membuat narasi puitis atau dramatis.
- Gunakan gaya bahasa akademik, natural, dan informatif.
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
    <ROLE>
    Anda adalah mesin analisis data kritis untuk Agentic Decision Support System (DSS) Pariwisata {destination}. Tugas Anda adalah mengekstrak SATU PARAGRAF keputusan tata kelola operasional yang bersumber MURNI dari data pengalaman wisatawan di bawah ini.
    </ROLE>
    
    <CRITICAL_RULES>
    1. OUTPUT HARUS LANGSUNG MASUK KE INTI ANALISIS. Kalimat pertama wajib langsung menyebutkan entitas pengelola atau kebijakan operasional (misal: "Pengelolaan...", "Manajemen...", "Otoritas...", "Kebijakan di {destination} harus...").
    2. DILARANG KERAS menggunakan kalimat pengantar seperti "Berikut adalah...", "Berdasarkan...", "Teks yang diperbaiki:".
    3. DILARANG KERAS berasumsi atau menambah narasi luar seperti: ekowisata, lingkungan, fasilitas sampah, masyarakat lokal, ekonomi, kesejahteraan, atau akses jalan. Jika kata tersebut TIKAK ADA di <STORYTELLING>, Anda akan gagal dalam tugas ini.
    4. NO GENERAL OPERATION BIAS: JANGAN memunculkan masalah standar pariwisata yang TIDAK TERTULIS di teks, seperti masalah "sampah", "kebersihan", "toilet", "keamanan", atau "petunjuk jalan". Fokus HANYA pada variabel eksplisit yang dipuji wisatawan.
    5. HANYA analisis aspek: kemegahan arsitektur, kenyamanan berjalan, kesejukan, dan estetika spot foto yang tertulis di teks.
    6. GAYA BAHASA: Gunakan huruf kecil yang normal di dalam kalimat (bukan HURUF KAPITAL di tengah kata), mengalir natural, analitis, bukan teks akademik klise, dan bukan cerita ulang.
    </CRITICAL_RULES>
    
    <STRICT_FORBIDDEN_WORDS>
    DILARANG KERAS menggunakan kata atau frasa berikut di seluruh teks (jika tertulis, sistem akan eror):
    - "dengan demikian"
    - "oleh karena itu"
    - "dapat disimpulkan"
    - "berdasarkan hal tersebut"
    - "kesimpulannya"
    - "sehingga" (di awal atau tengah kalimat yang berfungsi sebagai konjungsi kesimpulan robotik)
    - "hal ini dapat dilakukan" (frasa template pengisi kalimat)
    </STRICT_FORBIDDEN_WORDS>
    
    <OUTPUT_FORMAT>
    Wajib berbentuk SATU PARAGRAF pendek, maksimal 3 kalimat, padat, langsung pada solusi taktis manajemen objek wisata.
    </OUTPUT_FORMAT>
    """
    
        user_prompt = f"""
    <STORYTELLING>
    "{storytelling}"
    </STORYTELLING>
    
    <TASK>
    Tulis langsung hasil keputusan DSS.

    Jangan membuat judul.
    Jangan membuat pengantar.
    Jangan membuat label.
    Jangan menulis:
    "Berikut adalah..."
    "Berdasarkan data di atas..."
    "Hasil analisis..."
    "Analisis keputusan DSS..."
    
    Kalimat pertama HARUS langsung dimulai dengan:
    
    - Pengelolaan ...
    atau
    - Manajemen ...
    atau
    - Kebijakan ...
    
    Gunakan maksimal 3 kalimat.
    # Hasilkan analisis keputusan DSS dalam SATU PARAGRAF PADAT (maksimal 3 kalimat) untuk objek [{destination}] berdasarkan data <STORYTELLING> di atas.
    # #Ekstrak keputusan tata kelola operasional untuk destinasi [{destination}] berdasarkan data di dalam <STORYTELLING> di atas. 
        
    # LOGIKA STRUKTUR ANALISIS (Buat secara mengalir, jangan kaku):
    # - Kalimat 1: Sebutkan pihak pengelola/kebijakan dan tindakan prioritas utama untuk mempertahankan poin positif yang dirasakan wisatawan di <STORYTELLING>.
    # - Kalimat 2: Hubungkan tindakan tersebut dengan upaya menjaga atmosfer atau kenyamanan spesifik yang tertulis di teks.
    # - Kalimat 3: Berikan rekomendasi keputusan taktis di lapangan (misalnya terkait pengaturan spot foto, alur jalan, atau pemeliharaan fisik objek) agar kepuasan wisatawan tetap konsisten.
    
    # Ingat: Kosakata harus adaptif mengikuti variasi kata di dalam <STORYTELLING>, jangan gunakan template mati.
   
    # Sesuaikan kata sifat di atas murni menggunakan padanan kata dari <STORYTELLING>. Jangan kreatif menambah konsep luar!
    
    # Instruksi Tambahan: Buat hasil analisis yang serupa dengan contoh di atas, namun sesuaikan bahasanya secara dinamis mengikuti variasi kata kunci di dalam <STORYTELLING>. Jangan melantur ke isu umum pariwisata yang tidak ada di teks!
    </TASK>
    """
    
        result = call_llm(system_prompt, user_prompt)
        
        # Post-processing tambahan (Guardsafe) untuk memotong jika LLM masih nakal memberi pengantar
        # if ":" in result and len(result.split(":")[0]) < 30:
        #     result = result.split(":", 1)[1].strip()
        bad_prefixes = [
            "berikut adalah",
            "berdasarkan",
            "hasil analisis",
            "analisis keputusan",
            "hasil keputusan dss"
        ]
        
        for p in bad_prefixes:
            if result.lower().startswith(p):
                if ":" in result:
                    result = result.split(":", 1)[1].strip()
            
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
