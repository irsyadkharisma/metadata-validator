import streamlit as st
import pandas as pd
import requests
from io import BytesIO

if "data_source" not in st.session_state:
    st.session_state.data_source = None
    st.session_state.df = None

# Fields that are optional (allowed to be empty)
optional_fields = {
    "Kategori (Other)",
    "ID",
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

# ------------------------
# Validation Function
# ------------------------
def validate_metadata(df):
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

# ------------------------
# File Upload Handler
# ------------------------
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file and st.session_state.data_source is None:
    try:
        df = pd.read_excel(uploaded_file, sheet_name=0)
        st.session_state.df = df
        st.session_state.data_source = "file"
    except Exception as e:
        st.error(f"❗ Error reading file: {e}")

# ------------------------
# SharePoint/OneDrive Link Handler
# ------------------------
def fetch_excel_from_onedrive_or_sharepoint(shared_link):
    if "sharepoint.com" in shared_link and "download=1" not in shared_link:
        if "?" in shared_link:
            shared_link += "&download=1"
        else:
            shared_link += "?download=1"
    
    try:
        response = requests.get(shared_link, allow_redirects=True)
        response.raise_for_status()
        return pd.read_excel(BytesIO(response.content), engine='openpyxl')
    except Exception as e:
        raise Exception(f"Unable to read Excel from link: {e}")

link = st.text_input("Or Paste Excel Online Link (Permission must by Public/Anoyone, Be careful for sensitif data - sharepoint/onedrive) Link:")

# Clear Data button (using Streamlit native button)
if st.session_state.df is not None:
    if st.button("🧹 Clear Data"):
        st.session_state.clear()
        st.stop()

if link and st.session_state.data_source is None:
    try:
        df = fetch_excel_from_onedrive_or_sharepoint(link)
        st.session_state.df = df
        st.session_state.data_source = "link"
    except Exception as e:
        st.error(f"Failed to load file: {e}")

if st.session_state.df is not None:
    st.success("File loaded successfully!")
    st.dataframe(st.session_state.df.head())
    validate_metadata(st.session_state.df)