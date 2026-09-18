# 💼 Smart Company CareerMatch

**Smart Company CareerMatch** is a Python and Streamlit-based career assistant that helps job seekers discover relevant job opportunities, analyse their resumes, match skills with job requirements, create personalised preparation plans, and practise role-specific interview questions.

The application combines **Natural Language Processing (NLP), resume parsing, skill matching, public job sources, SQLite, and lightweight local RAG** into one career-preparation workflow.

## 🚀 Features

- 🔎 Natural-language job search
- 🏢 Company-specific job search
- 🌐 Public job-source integrations
- 📄 PDF, DOCX and TXT resume parsing
- 🧠 Skill extraction and NLP query processing
- 🎯 Resume-to-job skill matching
- 📊 Skill-gap identification
- 📚 Personalised preparation planning
- 🎤 100 interview-question generation
- 🤖 Lightweight local company-aware RAG
- 🗃️ SQLite job database support
- 🧪 Automated unit tests

## 🔄 Workflow

```text
User Search
    ↓
NLP Query Processing
    ↓
Live / Public Job Sources
    ↓
Job Results
    ↓
Resume Skill Analysis
    ↓
Resume ↔ Job Matching
    ↓
Missing Skill / Skill Gap
    ↓
Personalised Preparation
    ↓
100 Interview Questions
```

## 🛠️ Technologies

| Technology | Purpose |
|---|---|
| Python | Core application |
| Streamlit | Web interface |
| Requests | API/web requests |
| Regular Expressions | NLP and skill extraction |
| PyPDF | PDF resume extraction |
| python-docx | DOCX resume extraction |
| SQLite | Local database |
| Greenhouse | Public job source |
| Ashby | Public job source |
| Lever | Public job source |
| RAG | Local interview-question retrieval |
| unittest | Testing |

## 📁 Project Structure

```text
smart-company-careermatch/
│
├── app.py
├── database.py
├── interview.py
├── nlp_processor.py
├── preparation.py
├── resume_parser.py
├── skill_matcher.py
│
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── run_app.bat
│
├── job_sources/
│   ├── __init__.py
│   ├── aggregator.py
│   ├── ashby.py
│   ├── companies.py
│   ├── company_profiles.py
│   ├── fetcher.py
│   ├── greenhouse.py
│   ├── lever.py
│   └── official.py
│
└── tests/
    ├── __init__.py
    ├── test_core.py
    └── test_sources.py
```

## 📦 Installation

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/smart-company-careermatch.git
cd smart-company-careermatch
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## ▶️ Run

```powershell
python -m streamlit run app.py
```

Or on Windows:

```powershell
.\run_app.bat
```

## 🧪 Run Tests

```powershell
python -m unittest discover -s tests -v
```

## 🔎 Example Queries

```text
Python fresher jobs in Hyderabad
```

```text
TCS fresher jobs in Hyderabad
```

```text
backend Python jobs
```

```text
data analyst fresher jobs
```

## 📄 Resume Matching

Upload a resume in:

- PDF
- DOCX
- TXT

The application extracts configured skills and compares them with skills identified in selected job descriptions.

Example:

```text
Resume:
Python, SQL, HTML, CSS

Job:
Python, SQL, Django, REST API

Matching:
Python, SQL

Missing:
Django, REST API
```

## 🤖 Lightweight Local RAG

The interview module includes a lightweight retrieval mechanism for company-aware preparation.

It can combine:

- Company-specific questions
- Technical questions
- Resume-based questions
- HR questions
- Job-specific questions

This is a **local preparation system**, not a collection of confidential interview questions.

## ⚠️ Limitations

- Job availability depends on public source accessibility.
- Some career sites are JavaScript-heavy.
- Skill matching uses a configured skill vocabulary.
- Resume analysis is primarily text-based.
- The preparation planner uses a rule-based approach.
- The RAG component is lightweight local retrieval rather than a full vector-database/LLM pipeline.
- Users should verify current openings on the employer's official career portal before applying.

## 🔐 Security

Do not commit:

- API keys
- Passwords
- Personal resumes
- `.env` files containing secrets
- Local databases containing private information
- Virtual environments

The repository `.gitignore` is configured to help prevent common accidental commits.

## 🚀 Future Improvements

- Semantic/vector-based job matching
- Full vector-database RAG
- LLM-powered interview answers
- ATS resume scoring
- Automated skill-gap recommendations
- Job alerts
- Saved jobs
- Application tracking
- Interview answer evaluation
- Additional ATS integrations
- More official company career sources

## 👨‍💻 Project Highlights

- Built a Streamlit career-assistance application.
- Implemented natural-language job-query processing.
- Integrated multiple public job-source providers.
- Added resume parsing and skill extraction.
- Implemented resume-to-job skill matching.
- Added skill-gap analysis and preparation planning.
- Built a 100-question interview generation workflow.
- Added lightweight company-aware local RAG.
- Added automated unit tests.

## 📜 License

This project is licensed under the MIT License.

## ⭐ Support

If you find this project useful, consider giving the repository a star.
