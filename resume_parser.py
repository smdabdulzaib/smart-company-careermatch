import io
import re

SKILL_ALIASES = {
    "python": "Python", "java": "Java", "javascript": "JavaScript",
    "typescript": "TypeScript", "c++": "C++", "golang": "Golang",
    "go": "Go", "node.js": "Node.js", "node": "Node.js",
    "react": "React", "reactjs": "React", "django": "Django",
    "flask": "Flask", "fastapi": "FastAPI", "spring boot": "Spring Boot",
    "spring": "Spring", "hibernate": "Hibernate", "sql": "SQL",
    "mysql": "MySQL", "postgresql": "PostgreSQL", "mongodb": "MongoDB",
    "docker": "Docker", "kubernetes": "Kubernetes", "aws": "AWS",
    "azure": "Azure", "git": "Git", "github": "GitHub",
    "rest api": "REST API", "rest": "REST", "html": "HTML", "css": "CSS",
    "pandas": "Pandas", "numpy": "NumPy", "machine learning": "Machine Learning",
    "tensorflow": "TensorFlow", "pytorch": "PyTorch", "power bi": "Power BI",
    "excel": "Excel", "llms": "LLMs", "rag": "RAG",
    "prompt engineering": "Prompt Engineering"
}

def extract_resume_text(uploaded_file):
    name = uploaded_file.name.lower()
    data = uploaded_file.read()
    if name.endswith(".txt"):
        return data.decode("utf-8", errors="ignore")
    if name.endswith(".pdf"):
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(data))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except ImportError:
            raise RuntimeError("Install pypdf to read PDF resumes.")
    if name.endswith(".docx"):
        try:
            from docx import Document
            doc = Document(io.BytesIO(data))
            return "\n".join(p.text for p in doc.paragraphs)
        except ImportError:
            raise RuntimeError("Install python-docx to read DOCX resumes.")
    raise ValueError("Unsupported resume format.")

def extract_skills(text):
    low = text.lower()
    found = []
    for key, display in SKILL_ALIASES.items():
        if re.search(r"(?<!\w)" + re.escape(key) + r"(?!\w)", low):
            if display not in found:
                found.append(display)
    return found
