import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Playtest Dashboard SDD", layout="wide")
st.title("🛠️ Playtest: Data Cleaning")

st.sidebar.header("📂 Menu Upload Laporan")
# 1. Pintu masuk sekarang mengizinkan DUA jenis file
file_unggahan = st.sidebar.file_uploader("📂 Unggah file Laporan", type=["xlsx", "csv"])

if file_unggahan is not None:
    # 2. Sistem mengecek akhiran nama file
    nama_file = file_unggahan.name
    
    # ----------------------------------------------------
    # JALUR 1: JIKA FILE ADALAH CSV
    # ----------------------------------------------------
    if nama_file.endswith('.csv'):
        st.sidebar.success("Format CSV terdeteksi!")
        
        # Fitur pemotong baris tetap ada
        baris_dilewati = st.sidebar.slider("Jumlah baris dipotong dari atas:", 0, 30, 0)
        
        # Langsung baca menggunakan read_csv (Tanpa pilih sheet)
        df_mentah = pd.read_csv(file_unggahan, skiprows=baris_dilewati)
        sheet_pilihan = "Tabel CSV" # Nama default untuk tampilan judul nanti
        
    # ----------------------------------------------------
    # JALUR 2: JIKA FILE ADALAH EXCEL (XLSX)
    # ----------------------------------------------------
    elif nama_file.endswith('.xlsx'):
        st.sidebar.success("Format Excel terdeteksi!")
        
        # Baca nama-nama sheet dulu
        xls = pd.ExcelFile(file_unggahan)
        
        # Munculkan fitur pilih sheet
        sheet_pilihan = st.sidebar.selectbox("Pilih Sheet yang ingin dilihat:", xls.sheet_names)
        
        # Fitur pemotong baris
        baris_dilewati = st.sidebar.slider("Jumlah baris dipotong dari atas:", 0, 30, 0)
        
        # Baca menggunakan read_excel
        df_mentah = pd.read_excel(file_unggahan, sheet_name=sheet_pilihan, skiprows=baris_dilewati)

    # ==========================================
    # FASE PREVIEW & PEMBERSIHAN (Sama untuk keduanya)
    # ==========================================
    st.subheader(f"1. Preview Mentah - {sheet_pilihan}")
    st.dataframe(df_mentah)
    
    st.subheader("2. Hasil Pembersihan Dasar")
    df_bersih = df_mentah.dropna(how='all').dropna(axis=1, how='all')
    st.dataframe(df_bersih)

else:
    st.info("👈 Silakan unggah file Excel atau CSV di menu sebelah kiri.")

