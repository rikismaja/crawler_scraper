import asyncio
import aiohttp
from aiohttp import ClientTimeout
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.styles import Style
from prompt_toolkit.formatted_text import HTML
from pyfiglet import Figlet
from tqdm.asyncio import tqdm
import csv
import json
import argparse
import sys

# =======================================
# Banner
# =======================================
fig = Figlet(font='slant')
banner = fig.renderText('Crawler_Scraper')
print(banner)
print("ASYNC PRO by @rikismaja")
print("=" * 50)

# =======================================
# Konfigurasi Default
# =======================================
config = {
    "url": None,
    "depth": 2,
    "threads": 10,
    "delay": 0.5,
    "output": "hasil",
    "ignore_robots": False
}

# =======================================
# CLI Autocomplete
# =======================================
commands = ['set', 'show', 'run', 'help', 'exit', 'quit']
params = ['url', 'depth', 'threads', 'delay', 'output', 'ignore_robots']
shell_completer = WordCompleter(commands + params, ignore_case=True)

style = Style.from_dict({
    'prompt': '#00ff00 bold',
    '': '#ffffff'
})

session = PromptSession()

# =======================================
# HELP
# =======================================
def show_help():
    print("""
=============================================
🚀  Crawler_Scraper ASYNC PRO by @rikismaja
=============================================

Cara Penggunaan Dasar:
-----------------------
1️⃣  SET URL Target:
    set url https://example.com

2️⃣  SET Kedalaman Link (Depth):
    set depth 2

3️⃣  SET Jumlah Threads:
    set threads 5

4️⃣  SET Delay Antar Request:
    set delay 1.0

5️⃣  SET Output File Prefix:
    set output hasilku

6️⃣  (Optional) Abaikan robots.txt:
    set ignore_robots true

7️⃣  CEK Konfigurasi:
    show

8️⃣  JALANKAN CRAWLER:
    run

9️⃣  KELUAR:
    exit  atau  quit

Contoh Lengkap:
----------------
(crawler) > set url https://example.com
(crawler) > set depth 3
(crawler) > set threads 5
(crawler) > set delay 0.5
(crawler) > set output contoh
(crawler) > show
(crawler) > run

Hasil: contoh_urls.txt | contoh_urls.csv | contoh_urls.json

Selalu crawl dengan etika! 🚀

Perintah CLI langsung:
-----------------------
python crawler_scraper_async.py --url https://example.com --depth 2 --threads 20 --delay 0.2 --output hasil --ignore-robots
""")

# =======================================
# Show Config
# =======================================
def show_config():
    print("\n[ Konfigurasi Saat Ini ]")
    for k, v in config.items():
        print(f"  {k:<14}: {v}")
    print()

# =======================================
# Crawler Class
# =======================================
class AsyncCrawler:
    def __init__(self, start_url, max_depth, max_workers, delay, ignore_robots):
        self.start_url = start_url
        self.max_depth = max_depth
        self.max_workers = max_workers
        self.delay = delay
        self.ignore_robots = ignore_robots
        self.visited = set()
        self.results = []

    async def fetch(self, session, url):
        try:
            async with session.get(url) as response:
                return await response.text()
        except:
            return ""

    async def crawl(self):
        queue = [(self.start_url, 0)]
        conn = aiohttp.TCPConnector(limit_per_host=self.max_workers)
        timeout = ClientTimeout(total=15)
        async with aiohttp.ClientSession(connector=conn, timeout=timeout) as session:
            pbar = tqdm(total=1, desc="Crawling Progress")
            while queue:
                tasks = []
                for _ in range(min(len(queue), self.max_workers)):
                    url, depth = queue.pop(0)
                    if url in self.visited or depth > self.max_depth:
                        continue
                    self.visited.add(url)
                    tasks.append(self.worker(session, url, depth, queue))
                if tasks:
                    await asyncio.gather(*tasks)
                pbar.total = len(self.visited) + len(queue)
                pbar.update(len(tasks))
            pbar.close()

    async def worker(self, session, url, depth, queue):
        html = await self.fetch(session, url)
        soup = BeautifulSoup(html, 'html.parser')

        title_tag = soup.find('title')
        title = title_tag.text.strip() if title_tag else ""

        self.results.append({
            "url": url,
            "title": title,
            "depth": depth
        })

        for link in soup.find_all('a', href=True):
            abs_url = urljoin(url, link['href'])
            if abs_url.startswith(self.start_url) and abs_url not in self.visited:
                queue.append((abs_url, depth + 1))
        await asyncio.sleep(self.delay)

# =======================================
# Run Crawler
# =======================================
async def run_async_crawler():
    if not config['url']:
        print("❌ URL belum di-set.")
        return

    crawler = AsyncCrawler(
        start_url=config['url'],
        max_depth=config['depth'],
        max_workers=config['threads'],
        delay=config['delay'],
        ignore_robots=config['ignore_robots']
    )
    await crawler.crawl()

    print(f"\n✅ Selesai. Total ditemukan: {len(crawler.results)} halaman.")

    # Gunakan domain untuk output
    domain = urlparse(config['url']).netloc.replace('.', '_')
    prefix = f"{config['output']}_report_{domain}"

    # TXT
    txt_file = f"{prefix}.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        for item in crawler.results:
            f.write(f"{item['url']}\t{item['title']}\t{item['depth']}\n")

    # CSV
    csv_file = f"{prefix}.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['url', 'title', 'depth'])
        writer.writeheader()
        writer.writerows(crawler.results)

    # JSON
    json_file = f"{prefix}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(crawler.results, f, indent=2)

    print(f"[INFO] Hasil:\n  - {txt_file}\n  - {csv_file}\n  - {json_file}")

# =======================================
# Parse Argparse Mode CLI Langsung
# =======================================
def parse_cli_args():
    parser = argparse.ArgumentParser(description="Crawler_Scraper ASYNC PRO")
    parser.add_argument('--url', type=str, help='Target URL')
    parser.add_argument('--depth', type=int, help='Depth level')
    parser.add_argument('--threads', type=int, help='Max threads/workers')
    parser.add_argument('--delay', type=float, help='Delay in seconds')
    parser.add_argument('--output', type=str, help='Output prefix')
    parser.add_argument('--ignore-robots', action='store_true', help='Ignore robots.txt')

    args = parser.parse_args()

    if args.url:
        config['url'] = args.url
    if args.depth:
        config['depth'] = args.depth
    if args.threads:
        config['threads'] = args.threads
    if args.delay:
        config['delay'] = args.delay
    if args.output:
        config['output'] = args.output
    if args.ignore_robots:
        config['ignore_robots'] = True

    # Jika dijalankan dengan argumen, langsung run & exit
    if args.url:
        asyncio.run(run_async_crawler())
        sys.exit(0)

# =======================================
# Jalankan Argparse Dulu
# =======================================
parse_cli_args()

# =======================================
# MAIN LOOP INTERAKTIF
# =======================================
while True:
    try:
        user_input = session.prompt(
            HTML('<prompt>(crawler)</prompt> > '),
            completer=shell_completer,
            style=style
        )
        parts = user_input.strip().split()
        if not parts:
            continue
        cmd = parts[0]
        args = parts[1:]

        if cmd == 'set':
            if len(args) < 2:
                print("Usage: set [param] [value]")
                continue
            param, value = args[0], " ".join(args[1:])
            if param not in config:
                print(f"❌ Tidak dikenal: {param}")
                continue
            if param in ["depth", "threads"]:
                config[param] = int(value)
            elif param == "delay":
                config[param] = float(value)
            elif param == "ignore_robots":
                config[param] = value.lower() in ['true', '1', 'yes']
            else:
                config[param] = value
            show_config()

        elif cmd == 'show':
            show_config()

        elif cmd == 'run':
            asyncio.run(run_async_crawler())

        elif cmd == 'help':
            show_help()

        elif cmd in ['exit', 'quit']:
            print("Bye! 👋")
            break

        else:
            print(f"Perintah tidak dikenal: {cmd}. Ketik 'help'.")

    except KeyboardInterrupt:
        print("\nBye! 👋")
        break
    except EOFError:
        print("\nBye! 👋")
        break
