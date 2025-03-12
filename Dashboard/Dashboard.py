import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mplcursors
from babel.numbers import format_currency

# Load Data
file_path = "Dashboard/all_data.csv"

try:
    all_data = pd.read_csv(file_path, parse_dates = ["order_purchase_timestamp"])
except FileNotFoundError:
    st.error(f"File '{file_path}' tidak ditemukan. Pastikan file tersebut ada di direktori yang benar.")
    st.stop()

# Streamlit App
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# Sidebar Filters
st.sidebar.header("Filter Data")
selected_states = st.sidebar.multiselect("Pilih Wilayah:", sorted(all_data["customer_state"].dropna().unique()), default=[])
selected_products = st.sidebar.multiselect("Pilih Produk:", sorted(all_data["product_category_name_english"].dropna().unique()), default=[])

# Filter berdasarkan rentang tanggal
min_date = all_data["order_purchase_timestamp"].min()
max_date = all_data["order_purchase_timestamp"].max()
start_date, end_date = st.sidebar.date_input("Pilih Rentang Tanggal:", [min_date, max_date], min_value=min_date, max_value=max_date)

# Filter data berdasarkan pilihan pengguna
filtered_data = all_data[(all_data["order_purchase_timestamp"] >= pd.to_datetime(start_date)) &
                          (all_data["order_purchase_timestamp"] <= pd.to_datetime(end_date))]

if selected_states:
    filtered_data = filtered_data[filtered_data["customer_state"].isin(selected_states)]

if selected_products:
    filtered_data = filtered_data[filtered_data["product_category_name_english"].isin(selected_products)]

# Header
st.title("📊 E-Commerce Data Analysis Dashboard")


# ---- VISUALISASI 1: RFM ANALYSIS ----

# ---- Best Customers Based on Recency and Frequency Parameters ----
st.subheader("👤 Top Pelanggan Berdasarkan Parameter Recency dan Frequency")

# Cek apakah kolom penting tersedia
required_cols = ["order_purchase_timestamp", "customer_unique_id", "order_id", "total_order_value"]
if not all(col in filtered_data.columns for col in required_cols):
    st.warning("Data tidak memiliki kolom yang dibutuhkan untuk RFM Analysis.")
    st.stop()

# Menentukan tanggal referensi (tanggal terakhir dalam data terfilter)
reference_date = filtered_data["order_purchase_timestamp"].max()

# Hitung RFM
rfm_df = filtered_data.groupby("customer_unique_id").agg({
    "order_purchase_timestamp": lambda x: (reference_date - x.max()).days,
    "order_id": "nunique",
    "total_order_value": "sum"
}).reset_index()

# Rename kolom
rfm_df.columns = ["customer_unique_id", "Recency", "Frequency", "Monetary"]

# Hitung rata-rata
avg_recency = round(rfm_df["Recency"].mean(), 1)
avg_frequency = round(rfm_df["Frequency"].mean(), 2)
avg_monetary = format_currency(rfm_df["Monetary"].mean(), "BRL", locale='pt_BR')


# Tampilkan metrik
col1, col2 = st.columns(2)
col1.metric("📅 Average Recency (days)", avg_recency)
col2.metric("🛒 Average Frequency", avg_frequency)

# Visualisasi Top 5 Customer berdasarkan RFM
top5_recency = rfm_df.sort_values(by="Recency", ascending=True).head(5)
top5_frequency = rfm_df.sort_values(by="Frequency", ascending=False).head(5)

fig, ax = plt.subplots(1, 2, figsize=(30, 10))
colors = ["#69b3a2"] * 5

# Plot Recency
sns.barplot(y=top5_recency["Recency"], x=top5_recency["customer_unique_id"], palette=colors, ax=ax[0])
ax[0].set_title("Top 5 Pelanggan by Recency", fontsize=25)
ax[0].set_xlabel("Customer Unique ID", fontsize=20)
ax[0].set_ylabel("Recency (days)", fontsize=20)
ax[0].tick_params(axis='x', labelsize=15, rotation=45)
ax[0].tick_params(axis='y', labelsize=15)
ax[0].set_xticklabels(top5_recency["customer_unique_id"], rotation=45, ha="right")

# Plot Frequency (Pelanggan paling sering belanja)
sns.barplot(y=top5_frequency["Frequency"], x=top5_frequency["customer_unique_id"], palette=colors, ax=ax[1])
ax[1].set_title("Top 5 Pelanggan by Frequency", fontsize=25)
ax[1].set_xlabel("Customer Unique ID", fontsize=20)
ax[1].set_ylabel("Frequency (orders)", fontsize=20)
ax[1].tick_params(axis='x', labelsize=15, rotation=45)
ax[1].tick_params(axis='y', labelsize=15)
ax[1].set_xticklabels(top5_frequency["customer_unique_id"], rotation=45, ha="right")

st.pyplot(fig)


# ---- TOP 10 pelanggan dengan total belanja tertinggi ----
st.subheader("💰 Top 10 Pelanggan dengan Total Belanja (Monetary) Tertinggi")


st.metric("🛒 Average Monetary (BRL)", avg_monetary)

# Hitung total belanja per pelanggan
customer_spending_df = filtered_data.groupby("customer_unique_id").agg(
    total_spent=("total_order_value", "sum"),
    total_orders=("order_id", "nunique")
).reset_index()

# Ambil 10 pelanggan dengan total belanja tertinggi
top_customers_df = customer_spending_df.sort_values(by="total_spent", ascending=False).head(10).copy()

top_customers_df["category"] = ["Top 1" if i == 0 else "Lainnya" for i in range(len(top_customers_df))]
palette = {"Top 1": "darkblue", "Lainnya": "lightblue"}

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(
    x=top_customers_df["total_spent"],
    y=top_customers_df["customer_unique_id"],
    hue=top_customers_df["category"],
    dodge=False,
    palette=palette,
    ax=ax
)

for i, v in enumerate(top_customers_df["total_spent"]):
    ax.text(v + (0.01 * max(top_customers_df["total_spent"])), i, f"{v:,.0f}", va="center", fontsize=10)

ax.set_xlabel("Total Belanja (BRL)")
ax.set_ylabel("Customer Unique ID")
ax.set_title("Top 10 Pelanggan dengan Total Belanja Tertinggi")
ax.legend_.remove() 

mplcursors.cursor(ax, hover=True)

st.pyplot(fig)



# ---- VISUALISASI 3: WILAYAH DENGAN TINGKAT PEMBATALAN TERTINGGI ----
st.subheader("📍 Wilayah dengan Pembatalan Tinggi")

status_by_state_df = filtered_data.groupby(["customer_state", "order_status"]).size().unstack(fill_value=0)

if "canceled" in status_by_state_df.columns:
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ["darkblue" if i == 0 else "lightblue" for i in range(len(status_by_state_df["canceled"].sort_values(ascending=False)))]
    status_by_state_df["canceled"].sort_values(ascending=False).plot(kind="bar", color=colors, ax=ax)
    ax.set_xlabel("Wilayah")
    ax.set_ylabel("Jumlah Pembatalan")
    ax.set_title("Jumlah Pembatalan Pesanan per Wilayah")
    for i, v in enumerate(status_by_state_df["canceled"].sort_values(ascending=False)):
        ax.text(i, v + (0.01*max(status_by_state_df["canceled"])), str(v), ha='center', color='black')
        
    st.pyplot(fig)
else:
    st.warning("Tidak ada data pembatalan untuk wilayah yang dipilih.")

# ---- VISUALISASI 4: PRODUK DENGAN PENDAPATAN TERTINGGI & TERENDAH ----
st.subheader("📦 Produk dengan Pendapatan Tertinggi & Terendah")

product_revenue = filtered_data.groupby("product_category_name_english")["price"].sum().reset_index()
top_products_df = product_revenue.sort_values("price", ascending=False).head(10)
bottom_products_df = product_revenue.sort_values("price", ascending=True).head(10)

fig, ax = plt.subplots(1, 2, figsize=(20, 5))
colors_top = ["#008080" if i == 0 else "#20B2AA" for i in range(len(top_products_df))]
sns.barplot(
    data=top_products_df, 
    x="product_category_name_english", 
    y="price", 
    palette=colors_top, 
    ax=ax[0]
)

ax[0].set_xticklabels(ax[0].get_xticklabels(), rotation=45, ha="right")
ax[0].set_xlabel("Kategori Produk")
ax[0].set_ylabel("Pendapatan (BRL)")
ax[0].set_title("Top 10 Produk dengan Pendapatan Tertinggi")

for i, v in enumerate(top_products_df["price"]):
    ax[0].text(i, v + (0.01*max(top_products_df["price"])), str(int(v)), ha='center', color='black')

colors_bottom = ["#FF8C00" if i == 0 else "#FFA07A" for i in range(len(bottom_products_df))]
sns.barplot(
    data=bottom_products_df, 
    x="product_category_name_english", 
    y="price", 
    palette=colors_bottom, 
    ax=ax[1]
)

ax[1].set_xticklabels(ax[1].get_xticklabels(), rotation=45, ha="right")
ax[1].set_xlabel("Kategori Produk")
ax[1].set_ylabel("Pendapatan (BRL)")
ax[1].set_title("Top 10 Produk dengan Pendapatan Terendah")

for i, v in enumerate(bottom_products_df["price"]):
    ax[1].text(i, v + (0.01*max(bottom_products_df["price"])), str(int(v)), ha='center', color='black')

st.pyplot(fig)


# ---- VISUALISASI 5: JUMLAH TRANSAKSI PER BULAN ----
st.subheader("📅 Jumlah Transaksi Per Bulan")

filtered_data["year_month"] = filtered_data["order_purchase_timestamp"].dt.to_period("M")
transactions_per_month = filtered_data.groupby("year_month")["order_id"].count().reset_index()
transactions_per_month["year_month"] = transactions_per_month["year_month"].astype(str)

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=transactions_per_month, 
    x="year_month", 
    y="order_id", 
    marker="o", 
    color="b", 
    linewidth=2)

ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Transaksi")
ax.set_title("Tren Jumlah Transaksi Per Bulan")
plt.xticks(rotation=45)
st.pyplot(fig)

# Footer
st.markdown("**Dashboard by Aulaa Mustika_MC312D5X2481**")


