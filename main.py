import streamlit as st
import pandas as pd

# Fields that are optional (allowed to be empty)
optional_fields = {
    "Kategori (Other)",
    "ID",
    "Penafian (disclaimer) penggunaan data (Opsional)",
    "Lisensi Data / Ketentuan Penggunaan",
    "Lampirkan file lisensi",
    "Tim",
    "Aplikasi"
}

st.title("Irsyad Metadata Validator")
st.write("Upload your Excel file to validate mandatory metadata fields.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, sheet_name=0)
        df.columns = df.columns.str.strip()

        # Determine required columns
        all_columns = df.columns.tolist()
        required_fields = [col for col in all_columns if col not in optional_fields]

        # Check missing values
        st.subheader("Validation Results")

        has_issues = False

        for idx, row in df.iterrows():
            missing = [field for field in required_fields if pd.isna(row.get(field)) or str(row.get(field)).strip() == ""]
            if missing:
                has_issues = True
                st.warning(f"Row {idx + 2}: Missing fields: {', '.join(missing)}")  # +2 for header and 0-index
        if not has_issues:
            st.success("All required fields are filled ✅")
    except Exception as e:
        st.error(f"Error reading the file: {e}")
