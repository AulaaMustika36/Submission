# 📊 E-Commerce Data Analysis Dashboard

Dashboard ini dibangun menggunakan **Streamlit** untuk menganalisis data E-Commerce dari Brazil. Data mencakup informasi pesanan, pelanggan, produk, dan transaksi.

---
## 📦 Dataset

Data yang digunakan berasal dari Olist E-Commerce Dataset dari Brazil. 

Berdasarkan sumber tersebut, terdapat 5 dataset yang digunakan, yaitu:
- orders_dataset.csv
- order_items_dataset.csv
- customers_dataset.csv
- products_dataset.csv
- product_category_name_translation.csv

Asumsi file utama bernama `all_data.csv`.

---

## 🚀 Fitur Dashboard
1. **Filter Data**
    - Filter data berdasarkan Wilayah.
    - Filter data berdasarkan Kategori Produk.
    - Filter data berdasarkan Rentang Tanggal.

2. **Pendapatan Produk**
    - 10 Kategori Produk dengan Pendapatan Tertinggi.
    - 10 Kategori Produk dengan Pendapatan Terendah.

3. **Jumlah Pesanan Per Bulan**
    - Visualisasi jumlah pesanan per bulan untuk melihat pola pembelian dari tahun 2016-2018.

4. **Distribusi Status Pesanan** 
    - Visualisasi jumlah pesanan berdasarkan status pesananc(delivered, shipped, canceled, dll).

5. **Wilayah dengan Pembatalan Tertinggi**
    - Visualisasi jumlah pembatalan pesanan berdasarkan wilayah.
    
6. **RFM Analysis (Recency, Frequency, Monetary)**
    - Rata-rata Recency, Frequency, dan Monetary untuk semua pelanggan
    - Top 5 pelanggan berdasarkan Recency (Pelanggan terbaru berdasarkan hari sejak pembelian terakhir).
    - Top 5 pelanggan berdasarkan Frequency (Pelanggan dengan jumlah transaksi terbanyak).
    - Top 5 pelanggan berdasarkan Monetary (Pelanggan dengan total belanja tertinggi).


---

## 🛠️ Instalasi & Menjalankan Dashboard

### 1. **Clone repositori ini** (atau salin file ke folder lokal):
```bash
git clone https://github.com/username/nama-repo-kamu.git
cd nama-folder
```


**Buka folder proyek di lokal**

Pindahkan semua file proyek (termasuk `Dashboard.py` dan `all_data.csv`) ke dalam satu folder.

### 2. **Aktifkan Environment**
Buka Power Shell/Command Prompt/Terminal pada Visual Studio Code.

Setup Environment - Anaconda/Miniconda
```bash
conda create --name main-ds python=3.12.3
conda activate main-ds
```
Note: Sesuaikan dengan versi python Anda.

### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

atau install manual
```bash
pip install streamlit pandas matplotlib seaborn babel mplcursors
```

### 5. **Jalankan Dashboard**
```bash
streamlit run Dashboard.py
```
`Dashboard` adalah nama file Python yang berisi kode dashboard.

### 5. **Buka di browser**
Secara default, Streamlit akan membuka localhost di browser seperti:
```bash
hhttp://localhost:8501
```

---

## 📁 Struktur File
```bash
Submission
    Dashboard
        all_data.csv
        Dashboard.py
    Data
        customers_dataset.csv
        order_items_dataset.csv
        orders_dataset.csv
        product_category_name_translation.csv
        products_dataset.csv
    Proyek_Analisis_Data.ipynb
    README.md
    requirements.txt
    url.txt
```

---

## 📝 Catatan
- Pastikan file `all_data.csv` berada dalam direktori yang sama dengan file Python utama.

---

## 📚 Referensi
- Dahsboard ini terinspirasi dan dibangun dengan merujuk pada: Materi Dicoding: Belajar Analisis Data dengan Python
- Dashboard ini menggunakan dataset dari sumber : https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce 

---

## 👩‍💻 Author
**Aulaa Mustika**

Cohort ID: `MC312D5X2481`


