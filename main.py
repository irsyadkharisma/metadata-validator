import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Fields that are optional (allowed to be empty)
optional_fields = {
    "Kategori (Other)",
    "ID",
    "Skala atau resolusi spasial (Optional)",
    "Skala atau resolusi spasial (Optional)",
    "Penafian (disclaimer) penggunaan data (Opsional)",
    "Lisensi Data / Ketentuan Penggunaan",
    "Lampirkan file lisensi",
    "Tim",
    "Aplikasi"
}

st.title("WRI Metadata Validator")
st.write("Upload your Excel file to validate mandatory metadata fields.")
st.write("Unggah berkas Excel Anda untuk memvalidasi bidang metadata wajib.")
st.write("contact: irsyad.kharisma@wri.org")


#FILE
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, sheet_name=0)
        df.columns = df.columns.str.strip()

        required_fields = [col for col in df.columns if col not in optional_fields]

        st.subheader("Results/Hasil Pengecekan File")

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
            st.success("All mandatory fields are filled correctly ✅")
            st.success("Semua kolom wajib terisi dengan benar ✅")

    except Exception as e:
        st.error(f"❗ Error read file: {e}")

#LINK
def fetch_excel_from_onedrive_or_sharepoint(shared_link):
    # Add download=1 if it's SharePoint-style link
    if "sharepoint.com" in shared_link and "download=1" not in shared_link:
        if "?" in shared_link:
            shared_link += "&download=1"
        else:
            shared_link += "?download=1"
    
    try:
        response = requests.get(shared_link, allow_redirects=True)
        response.raise_for_status()  # raises error for 4xx/5xx

        try:
            # Try to parse Excel with openpyxl
            return pd.read_excel(BytesIO(response.content), engine='openpyxl')
        except Exception as parse_error:
            raise Exception("Downloaded file could not be parsed as Excel. Are you sure it's an .xlsx file?") from parse_error

    except Exception as e:
        raise e

import streamlit as st

st.title("Metadata Validator")

link = st.text_input("Paste Excel Online (OneDrive/SharePoint) Link:")

if link:
    try:
        df = fetch_excel_from_onedrive_or_sharepoint(link)
        st.success("File loaded successfully!")
        st.dataframe(df.head())
    except Exception as e:
        st.error(f"Failed to load file: {e}")