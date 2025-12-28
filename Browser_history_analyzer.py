import os
import sys
import sqlite3
import shutil
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qs

# ================= OUTPUT TO FILE + TERMINAL =================
class TeeOutput:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.file = open(filename, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.file.write(message)

    def flush(self):
        self.terminal.flush()
        self.file.flush()

# ================= GET NEXT FILE NUMBER =================
def get_next_report_number():
    files = os.listdir(".")
    numbers = []

    for f in files:
        if f.startswith("Chrome_Forensic_Report_") and f.endswith(".txt"):
            try:
                num = int(f.replace("Chrome_Forensic_Report_", "").replace(".txt", ""))
                numbers.append(num)
            except ValueError:
                pass

    return max(numbers) + 1 if numbers else 1

# ================= TIME CONVERSION =================
def chrome_time_to_datetime(chrome_time):
    if chrome_time == 0:
        return "N/A"
    return (datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)) \
        .strftime("%Y-%m-%d %H:%M:%S")

# ================= SEARCH EXTRACTION =================
def extract_search(url, title):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    if "google." in parsed.netloc and "q" in params:
        return "Google", params["q"][0]

    if "youtube.com" in parsed.netloc and "search_query" in params:
        return "YouTube", params["search_query"][0]

    if "amazon." in parsed.netloc and "k" in params:
        return "Amazon", params["k"][0]

    if "chatgpt.com" in parsed.netloc and title:
        return "ChatGPT", title

    return None, None

# ================= BANNER =================
def banner():
    print("""
╔════════════════════════════════════════════════════════════╗
║      🌐 CHROME SEARCH HISTORY ANALYZER (FORENSICS)         ║
╠════════════════════════════════════════════════════════════╣
║ Investigator : Dhruvik Variya                               ║
║ OS           : Kali Linux                                  ║
║ Browser      : Google Chrome                               ║
╚════════════════════════════════════════════════════════════╝
""")

# ================= SEARCH HISTORY =================
def analyze_search_history():
    print("\n🔍 SEARCH HISTORY (Including ChatGPT)")
    print("─" * 62)

    conn = sqlite3.connect("History_copy")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT url, title, last_visit_time
        FROM urls
        ORDER BY last_visit_time DESC
    """)

    count = 1
    for url, title, time in cursor.fetchall():
        engine, query = extract_search(url, title)
        if engine and query:
            print(f"[{count:02}] 🕒 {chrome_time_to_datetime(time)}")
            print(f"     🔍 Engine : {engine}")
            print(f"     🔑 Query  : {query}")
            print("─" * 62)
            count += 1
        if count > 20:
            break

    conn.close()

# ================= VISITED WEBSITES =================
def analyze_visited_sites():
    print("\n🌐 VISITED WEBSITES (Last 20)")
    print("─" * 62)

    conn = sqlite3.connect("History_copy")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT url, title, visit_count, last_visit_time
        FROM urls
        WHERE url NOT LIKE '%oauth%'
        AND url NOT LIKE '%accounts.google%'
        ORDER BY last_visit_time DESC
        LIMIT 20
    """)

    for i, (url, title, visits, time) in enumerate(cursor.fetchall(), 1):
        domain = urlparse(url).netloc
        print(f"[{i:02}] 🕒 {chrome_time_to_datetime(time)}")
        print(f"     🌍 Site   : {domain}")
        print(f"     📄 Title  : {title}")
        print(f"     🔢 Visits : {visits}")
        print("─" * 62)

    conn.close()

# ================= MAIN =================
def main():
    report_number = get_next_report_number()
    output_file = f"Chrome_Forensic_Report_{report_number}.txt"

    sys.stdout = TeeOutput(output_file)

    banner()

    history_path = os.path.expanduser("~/.config/google-chrome/Default/History")

    if not os.path.exists(history_path):
        print("❌ Chrome history file not found")
        return

    shutil.copy(history_path, "History_copy")

    analyze_search_history()
    analyze_visited_sites()

    print("\n✔ ChatGPT Queries Derived from Page Titles")
    print("✔ Forensic Integrity Maintained")
    print("✔ Analysis Completed Successfully")
    print(f"📁 Report saved as: {output_file}\n")

if __name__ == "__main__":
    main()
