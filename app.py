import streamlit as st
import pandas as pd
import io  # <--- Tambahkan baris ini (Ini adalah 'flashdisk virtual' kita)

# Mengatur tampilan layar web
st.set_page_config(page_title="Playtest Dashboard SDD", layout="wide")

st.title("🛠️ Playtest: Pembersih Data DBoards 2025")
st.write("Ini adalah purwarupa (prototype) untuk melihat bagaimana file Excel multi-sheet Anda dibersihkan dan diolah.")
st.markdown("---")

# Menu Upload di Samping
st.sidebar.header("📂 Menu Upload Laporan")
file_unggahan = st.sidebar.file_uploader("📂 Unggah file Excel Laporan di sini", type=["xlsx"])

if file_unggahan is not None:
    # 1. Membaca seluruh nama Sheet yang ada di dalam Excel
    xls = pd.ExcelFile(file_unggahan)
    nama_sheets = xls.sheet_names
    
    # 2. Fitur Interaktif: Biarkan pengguna memilih sheet untuk di-playtest
    sheet_pilihan = st.sidebar.selectbox("Pilih Sheet yang ingin dilihat:", nama_sheets)    
    
    # 3. Fitur Interaktif: Slider untuk melompati baris kotor di atas tabel (skiprows)
    # Karena tadi ada sheet yang butuh dilompati hingga 25 baris
    baris_dilewati = st.sidebar.slider("Jumlah baris keterangan yang ingin dipotong dari atas:", 0, 30, 0)
    
    # Membaca data berdasarkan sheet dan baris yang dipotong
    df_mentah = pd.read_excel(file_unggahan, sheet_name=sheet_pilihan, skiprows=baris_dilewati)
    
    # ==========================================
    # FASE PREVIEW MENTAH
    # ==========================================
    st.subheader(f"1. Preview Mentah - Sheet: {sheet_pilihan}")
    st.write("Tampilan data setelah baris atas dipotong sesuai slider:")
    st.dataframe(df_mentah.head(15)) # Menampilkan 15 baris pertama
    
    # ==========================================
    # FASE PEMBERSIHAN OTOMATIS
    # ==========================================
    st.subheader("2. Hasil Pembersihan Dasar")
    
    # Logika pembersihan: Menghapus baris/kolom yang KOSONG TOTAL
    # (Sering terjadi di Excel jika ada sisa format warna/garis tanpa teks)
    df_bersih = df_mentah.dropna(how='all').dropna(axis=1, how='all')
    
   # ... (kode sebelumnya)
    st.write("Data setelah baris dan kolom yang benar-benar kosong dibersihkan oleh sistem:")
    st.dataframe(df_bersih.head(15))
    
    # ==========================================
    # FASE UNDUH EXCEL (XLSX)
    # ==========================================
    st.subheader("📥 Unduh Hasil Pembersihan")
    
    # 1. Menyiapkan 'flashdisk virtual' di memori
    buffer = io.BytesIO()
    
    # 2. Menyuruh Pandas menyimpan data bersih ke dalam flashdisk virtual tersebut
    # index=False agar nomor urut 0, 1, 2 bawaan Python tidak ikut tersimpan
    df_bersih.to_excel(buffer, index=False, engine='openpyxl')
    
    # 3. Membuat tombol unduh resmi dari Streamlit
    st.download_button(
        label="Download Data Bersih (.xlsx)",
        data=buffer.getvalue(), # Mengambil isi dari flashdisk virtual
        file_name=f"Data_Bersih_{sheet_pilihan}.xlsx", # Nama file otomatis sesuai nama sheet
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" # Kode standar web untuk file Excel
    )
     

else:
    st.info("👈 Silakan unggah file Anda di menu sebelah kiri untuk memulai playtest.")
