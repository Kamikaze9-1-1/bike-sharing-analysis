import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ===================== CONFIG =====================
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚴",
    layout="wide"
)

# ===================== LOAD DATA =====================
@st.cache_data
def load_data():
    df = pd.read_csv('data/day.csv')
    df['dteday'] = pd.to_datetime(df['dteday'])
    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weathersit_map = {1: 'Clear', 2: 'Cloudy', 3: 'Light Rain/Snow', 4: 'Heavy Rain/Snow'}
    workingday_map = {0: 'Holiday/Weekend', 1: 'Working Day'}
    df['season_label'] = df['season'].map(season_map)
    df['weathersit_label'] = df['weathersit'].map(weathersit_map)
    df['workingday_label'] = df['workingday'].map(workingday_map)
    df['temp_celsius'] = df['temp'] * 41
    df['hum_pct'] = df['hum'] * 100
    df['windspeed_kph'] = df['windspeed'] * 67
    df['yr_label'] = df['yr'].map({0: '2011', 1: '2012'})
    return df

df = load_data()

# ===================== SIDEBAR =====================
st.sidebar.title("🚴 Bike Sharing")
st.sidebar.markdown("**Filter Data**")

year_options = ['Semua', '2011', '2012']
selected_year = st.sidebar.selectbox("Tahun", year_options)

season_options = ['Semua'] + list(df['season_label'].unique())
selected_season = st.sidebar.multiselect("Musim", df['season_label'].unique(),
                                          default=list(df['season_label'].unique()))

# Filter
filtered = df.copy()
if selected_year != 'Semua':
    filtered = filtered[filtered['yr_label'] == selected_year]
if selected_season:
    filtered = filtered[filtered['season_label'].isin(selected_season)]

# ===================== HEADER =====================
st.title("🚴 Dashboard Analisis Bike Sharing")
st.markdown("**Proyek Analisis Data** | Dicoding Data Analysis")
st.markdown("---")

# ===================== METRICS =====================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Penyewaan", f"{filtered['cnt'].sum():,.0f}")
col2.metric("Rata-rata Harian", f"{filtered['cnt'].mean():,.0f}")
col3.metric("Penyewaan Tertinggi", f"{filtered['cnt'].max():,.0f}")
col4.metric("Penyewaan Terendah", f"{filtered['cnt'].min():,.0f}")

st.markdown("---")

# ===================== CHART 1: Tren Harian =====================
st.subheader("📈 Tren Penyewaan Harian")
fig1, ax1 = plt.subplots(figsize=(12, 4))
ax1.plot(filtered['dteday'], filtered['cnt'], color='#3498db', linewidth=1, alpha=0.8)
ax1.fill_between(filtered['dteday'], filtered['cnt'], alpha=0.2, color='#3498db')
ax1.set_xlabel("Tanggal")
ax1.set_ylabel("Jumlah Penyewaan")
ax1.grid(alpha=0.3)
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
plt.tight_layout()
st.pyplot(fig1)

# ===================== CHART 2 & 3 =====================
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("🌤️ Pengaruh Cuaca terhadap Penyewaan")
    cuaca_avg = filtered.groupby('weathersit_label')['cnt'].mean().sort_values(ascending=False)
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    colors = ['#f1c40f', '#95a5a6', '#3498db', '#2c3e50']
    bars = ax2.barh(cuaca_avg.index, cuaca_avg.values, color=colors[:len(cuaca_avg)], edgecolor='white')
    ax2.set_xlabel("Rata-rata Penyewaan")
    ax2.grid(axis='x', alpha=0.3)
    for bar, val in zip(bars, cuaca_avg.values):
        ax2.text(val + 50, bar.get_y() + bar.get_height()/2,
                 f'{val:.0f}', va='center', fontsize=9)
    plt.tight_layout()
    st.pyplot(fig2)

with col_b:
    st.subheader("🍂 Penyewaan per Musim")
    season_order = ['Spring', 'Summer', 'Fall', 'Winter']
    season_avg = filtered.groupby('season_label')['cnt'].mean().reindex(
        [s for s in season_order if s in filtered['season_label'].unique()]
    )
    fig3, ax3 = plt.subplots(figsize=(6, 4))
    colors3 = ['#2ecc71', '#f39c12', '#e74c3c', '#3498db']
    bars3 = ax3.bar(season_avg.index, season_avg.values, color=colors3[:len(season_avg)],
                    edgecolor='white', linewidth=1.5)
    ax3.set_ylabel("Rata-rata Penyewaan")
    ax3.grid(axis='y', alpha=0.3)
    for bar, val in zip(bars3, season_avg.values):
        ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
                 f'{val:.0f}', ha='center', fontsize=9, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig3)

# ===================== CHART 4: Hari Kerja vs Libur =====================
st.subheader("📅 Hari Kerja vs Hari Libur/Akhir Pekan")
col_c, col_d = st.columns([1, 2])

with col_c:
    wd_avg = filtered.groupby('workingday_label')['cnt'].mean()
    st.dataframe(wd_avg.rename("Rata-rata Penyewaan").reset_index(), use_container_width=True)

with col_d:
    pivot = filtered.pivot_table(values='cnt', index='season_label',
                                  columns='workingday_label', aggfunc='mean')
    season_order_avail = [s for s in season_order if s in pivot.index]
    pivot = pivot.reindex(season_order_avail)
    fig4, ax4 = plt.subplots(figsize=(8, 4))
    x = np.arange(len(pivot.index))
    width = 0.35
    if 'Holiday/Weekend' in pivot.columns:
        ax4.bar(x - width/2, pivot['Holiday/Weekend'], width, label='Holiday/Weekend',
                color='#e74c3c', alpha=0.85)
    if 'Working Day' in pivot.columns:
        ax4.bar(x + width/2, pivot['Working Day'], width, label='Working Day',
                color='#3498db', alpha=0.85)
    ax4.set_xticks(x)
    ax4.set_xticklabels(pivot.index)
    ax4.set_ylabel("Rata-rata Penyewaan")
    ax4.legend()
    ax4.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig4)

st.markdown("---")
st.caption("Dashboard dibuat oleh [Nama Anda] | Proyek Analisis Data Dicoding")
