import streamlit as st
import pandas as pd
import unicodedata

# Normalize text (handles extra spaces, non-breaking spaces, invisible characters)
def normalize(text):
    if not isinstance(text, str):
        return text
    return unicodedata.normalize("NFKC", text.strip())

# Define optional fields (normalized)
optional_fields = set(map(normalize, [
    "Kategori (Other)",
    "ID",
    "Skala atau resolusi spasial (Optional)",
    "Penafian (disclaimer) penggunaan data (Opsional)",
    "Lisensi Data / Ketentuan Penggunaan",
    "Lampirkan file lisensi",
    "Tim",
    "Aplikasi"
]))

st.title("WRI Metadata Validator")
st.write("Upload your Excel file to validate mandatory metadata fields.")
st.write("Unggah berkas Excel Anda untuk memvalidasi bidang metadata wajib.")
st.write("Contact: irsyad.kharisma@wri.org")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, sheet_name=0)
        df.columns = [normalize(c) for c in df.columns]

        required_fields = [col for col in df.columns if col not in optional_fields]

        st.subheader("Hasil Pengecekan File")

        has_issues = False

        for idx, row in df.iterrows():
            missing = [
                field for field in required_fields
                if pd.isna(row.get(field)) or str(row.get(field)).strip() == ""
            ]

            if missing:
                has_issues = True
                judul = str(row.get("Judul", "")).strip()
                st.warning(
                    f"🔎 Baris {idx + 2} — **Judul/Nama Data**: *{judul or 'Tidak ada judul'}*\n"
                    f"❌ Kosong pada kolom: {', '.join(missing)}"
                )

        if not has_issues:
            st.success("Semua kolom wajib terisi dengan benar ✅")

    except Exception as e:
        st.error(f"❗ Error membaca file: {e}")
