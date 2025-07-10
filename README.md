# 🚀 Crawler_Scraper ASYNC PRO by @pyshc

**Crawler_Scraper ASYNC PRO** adalah **web crawler** super ringan & cepat, dibuat dengan **Python**, memanfaatkan **`asyncio` + `aiohttp`** untuk scanning ribuan halaman dengan efisien.  
Dilengkapi antarmuka **CLI interaktif** _dan_ **mode argumen langsung**, serta menyimpan hasil dalam format **TXT**, **CSV**, dan **JSON**.

---

## ✨ **Fitur Utama**

- 🔗 **Crawl recursive link** dengan `depth` & `delay` custom
- ⚡ **Async HTTP requests** ➜ lebih cepat & ringan dari `requests`
- 🔒 **Mode hormat `robots.txt`** (bisa abaikan dengan `--ignore-robots`)
- ✅ **Dual Mode**: Interaktif (`prompt_toolkit`) & CLI argumen (`argparse`)
- 📑 **Output lengkap** ➜ `url + title + depth` ➜ simpan ke **TXT, CSV, JSON**
- 🛡️ Cocok untuk **pentest** & **recon**

---

## 📦 **Dependencies**

Pastikan Python 3.8+ & install:

pip install aiohttp beautifulsoup4 tqdm prompt_toolkit pyfiglet

'''
## ⚙️ Cara Jalankan
1️⃣ Mode Interaktif
python crawler_scraper_async.py
Contoh alur perintah:
(crawler) > set url https://example.com
(crawler) > set depth 2
(crawler) > set threads 20
(crawler) > set delay 0.2
(crawler) > set ignore_robots true
(crawler) > run

## 📌 Perintah Tersedia

set [param] [value] ➜ atur parameter (url, depth, threads, delay, output, ignore_robots)

show ➜ tampilkan konfigurasi aktif

run ➜ mulai crawling

help ➜ tampilkan panduan

exit ➜ keluar

## 2️⃣ Mode Argumen Langsung
Jalankan tanpa menu interaktif:
python crawler_scraper_async.py \
  --url https://example.com \
  --depth 2 \
  --threads 20 \
  --delay 0.2 \
  --output hasil \
  --ignore-robots
## 📁 Output
File output otomatis memakai nama domain target:
hasil_report_example_com.txt
hasil_report_example_com.csv
hasil_report_example_com.json

## Struktur data:
url	title	depth

⚠️ Etika Penggunaan
🚫 Gunakan hanya untuk domain yang Anda miliki hak aksesnya atau untuk tujuan pembelajaran / audit yang sah.
Crawler cepat & asinkron dapat membebani server target jika tidak diatur delay & threads secara wajar.

📌 Kontributor
Made with ❤️ by @pyshc
