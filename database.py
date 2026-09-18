import sqlite3

DB_PATH = "data/company_hiring.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT, title TEXT, location TEXT, experience TEXT,
        skills TEXT, description TEXT, source_url TEXT, apply_url TEXT,
        UNIQUE(company, title, location, source_url)
    )""")
    conn.commit()
    conn.close()

def save_jobs(jobs):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    for j in jobs:
        conn.execute("""INSERT OR IGNORE INTO jobs
        (company,title,location,experience,skills,description,source_url,apply_url)
        VALUES (?,?,?,?,?,?,?,?)""", (
            j.get("company",""), j.get("title",""), j.get("location",""),
            j.get("experience",""), j.get("skills",""), j.get("description",""),
            j.get("source_url",""), j.get("apply_url","")
        ))
    conn.commit()
    conn.close()
