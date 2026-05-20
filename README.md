# Proyek Analisis Data: Bike Sharing Dataset

## Deskripsi Proyek
Proyek ini merupakan analisis data terhadap Bike Sharing Dataset untuk menjawab pertanyaan bisnis berikut:
1. Faktor cuaca apa saja yang paling mempengaruhi jumlah penyewaan sepeda harian?
2. Bagaimana pola penyewaan sepeda berdasarkan hari kerja vs hari libur dan musim?

## Struktur Direktori
```
submission/
├── dashboard/
│   ├── dashboard.py
│   └── day.csv
├── data/
│   └── day.csv
├── notebook.ipynb
├── requirements.txt
└── url.txt
```

## Cara Menjalankan Dashboard
1. Install dependencies:
```
pip install -r requirements.txt
```
2. Jalankan dashboard:
```
streamlit run dashboard/dashboard.py
```

## Dataset
- **Sumber:** [Bike Sharing Dataset - UCI ML Repository](https://archive.ics.uci.edu/ml/datasets/bike+sharing+dataset)
- **File yang digunakan:** `day.csv`
