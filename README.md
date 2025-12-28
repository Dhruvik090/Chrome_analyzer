# 🕵️ Chrome Browser History Analyzer (Forensics)

A **Python-based digital forensics tool** that extracts and analyzes **Google Chrome browsing and search history** from a forensic investigation perspective.  
Designed for **Cybersecurity students, SOC analysts, and Digital Forensics professionals** while maintaining evidence integrity.

---

## ✨ Features

| Feature | Description |
|------|-------------|
| 🔍 Search Analysis | Extracts last 20 search queries from Google, YouTube, Amazon & ChatGPT |
| 🌐 Website Analysis | Displays last 20 visited websites |
| 🕒 Timestamp Conversion | Converts Chrome timestamps to readable date & time |
| 📄 Report Generation | Automatically generates forensic report (.txt) |
| 🖥️ Dual Output | Prints output to terminal and report file |
| 🛡️ Forensic Integrity | Analyzes a copied history database |

---

## 🎯 Forensic Relevance

This tool is useful for:

- Browser forensics
- Incident response investigations
- User activity reconstruction
- Academic and lab demonstrations
- SOC analyst training
- Educational cybercrime investigations

⚠️ **Note:** Authorized and educational use only.

---

## 🛠️ Requirements

| Component | Details |
|--------|---------|
| OS | Linux (Tested on Kali Linux) |
| Python | Python 3.x |
| Browser | Google Chrome |
| Libraries | Built-in Python modules only |

### 📦 Built-in Python Modules

| Module | Purpose |
|------|---------|
| sqlite3 | Access Chrome history database |
| shutil | Create forensic copy |
| datetime | Timestamp conversion |
| urllib.parse | Search query extraction |

---

## 🚀 Installation

```bash
git clone https://github.com/Dhruvik090/Browser-History-Analyzer.git
cd Browser-History-Analyzer
```

---

## ▶️ Usage

```bash
python3 Browser_history_analyzer.py
```

---

## 📂 Output

### 🧾 Generated Reports
```
Chrome_Forensic_Report_1.txt
Chrome_Forensic_Report_2.txt
```

### 🔍 Sample Search History Output
```
[01] 🕒 2025-12-27 17:19:01
     🔍 Engine : Google
     🔑 Query  : amazon laptop
------------------------------------------------------------

[02] 🕒 2025-12-27 16:46:51
     🔍 Engine : YouTube
     🔑 Query  : cyber security roadmap
------------------------------------------------------------
```

### 🌐 Sample Visited Websites Output
```
[01] 🕒 2025-12-27 16:46:51
     🌍 Site   : www.youtube.com
     📄 Title  : YouTube
     🔢 Visits : 125
------------------------------------------------------------
```

---

## 🔐 Forensic Methodology

- Chrome History SQLite database analysis
- Evidence duplication using `History_copy`
- Read-only forensic examination
- Timeline-based activity reconstruction
- URL parameter-based search extraction

---

## 📘 Learning Outcomes

- Understand browser forensic artifacts
- Perform Chrome SQLite database analysis
- Apply Python scripting in cybersecurity
- Practice real-world forensic investigation techniques

---

## 👨‍💻 Author

**Dhruvik Variya**  
🎓 MSc IT (Cybersecurity & Digital Forensics)  
🛡️ Cybersecurity Student  

---

## ⚖️ Disclaimer

This project is developed strictly for **educational and ethical purposes**.  
Unauthorized access or misuse of personal data is illegal.
