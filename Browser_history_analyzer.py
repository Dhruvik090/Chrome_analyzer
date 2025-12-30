#!/usr/bin/env python3

import os
import sys
import sqlite3
import shutil
import argparse
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


# ================= TIME CONVERSION =================
def chrome_time_to_datetime(chrome_time):
    if chrome_time == 0:
        return "N/A"
    return (
        datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)
    ).strftime("%Y-%m-%d %H:%M:%S")


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
def analyze_search_history(limit):
    print("\n🔍 SEARCH HISTORY")
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

        if count > limit:
            break

    conn.close()


# ================= VISITED WEBSITES =================
def analyze_visited_sites(limit):
    print(f"\n🌐 VISITED WEBSITES (Last {limit})")
    print("─" * 62)

    conn = sqlite3.connect("History_copy")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT url, title, visit_count, last_visit_time
        FROM urls
        WHERE url NOT LIKE '%oauth%'
        AND url NOT LIKE '%accounts.google%'
        ORDER BY last_visit_time DESC
        LIMIT ?
    """, (limit,))

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
    parser = argparse.ArgumentParser(
        description="Chrome Browser History Forensic Analyzer"
    )

    parser.add_argument(
        "-s", "--search",
        type=int,
        default=20,
        help="Number of search queries"
    )

    parser.add_argument(
        "-v", "--visited",
        type=int,
        default=20,
        help="Number of visited sites"
    )

    parser.add_argument(
        "-o", "--output",
        help="Output report filename"
    )

    args = parser.parse_args()

    if args.output:
        sys.stdout = TeeOutput(args.output)

    banner()

    base_path = os.path.expanduser("~/.config/google-chrome")

    if not os.path.exists(base_path):
        print("❌ Chrome directory not found")
        return

    profiles = [
        p for p in os.listdir(base_path)
        if p == "Default" or p.startswith("Profile")
    ]

    if not profiles:
        print("❌ No Chrome profiles found")
        return

    for profile in profiles:
        history_path = os.path.join(base_path, profile, "History")

        if not os.path.exists(history_path):
            continue

        print(f"\n📂 Analyzing Profile: {profile}")

        shutil.copy(history_path, "History_copy")

        analyze_search_history(args.search)
        analyze_visited_sites(args.visited)

    print("\n✔ Forensic Analysis Completed Successfully")


if __name__ == "__main__":
    main()
